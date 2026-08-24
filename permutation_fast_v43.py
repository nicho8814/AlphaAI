import requests
import time
import math
import numpy as np


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "NEARUSDT",
    "AVAXUSDT",
    "SUIUSDT",
    "APTUSDT",
    "ARBUSDT",
    "TIAUSDT",
    "AAVEUSDT",
    "ATOMUSDT",
]

URL = "https://api.binance.com/api/v3/klines"

INTERVAL = "1h"
TOTAL_CANDLES = 5000
BATCH_SIZE = 1000

HORIZON = 6
N_FOLDS = 4
MIN_TRAIN = 1000

LEARNING_RATE = 0.03
EPOCHS = 250
L2 = 0.001

N_PERMUTATIONS = 1000
SEED = 420


def sigmoid(x):
    x = np.clip(x, -40, 40)
    return 1.0 / (1.0 + np.exp(-x))


def get_candles(symbol, limit=1000, end_time=None):

    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "limit": limit,
    }

    if end_time is not None:
        params["endTime"] = end_time

    r = requests.get(
        URL,
        params=params,
        timeout=20,
    )

    r.raise_for_status()

    data = r.json()

    candles = []

    for row in data:
        candles.append({
            "time": int(row[0]),
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "volume": float(row[5]),
        })

    candles.sort(
        key=lambda x: x["time"]
    )

    return candles


def download_history(symbol):

    collected = []
    end_time = None

    while len(collected) < TOTAL_CANDLES:

        remaining = (
            TOTAL_CANDLES
            - len(collected)
        )

        limit = min(
            BATCH_SIZE,
            remaining,
        )

        batch = get_candles(
            symbol,
            limit,
            end_time,
        )

        if not batch:
            break

        collected.extend(batch)

        end_time = (
            batch[0]["time"] - 1
        )

        if len(batch) < BATCH_SIZE:
            break

        time.sleep(0.10)

    unique = {
        x["time"]: x
        for x in collected
    }

    result = list(
        unique.values()
    )

    result.sort(
        key=lambda x: x["time"]
    )

    return result[-TOTAL_CANDLES:]


def safe_return(candles, i, bars):

    if i - bars < 0:
        return 0.0

    old = candles[
        i - bars
    ]["close"]

    current = candles[
        i
    ]["close"]

    if old <= 0:
        return 0.0

    return (
        current - old
    ) / old * 100.0


def volatility(candles, i, bars):

    values = []

    start = max(
        1,
        i - bars + 1,
    )

    for j in range(
        start,
        i + 1,
    ):

        old = candles[
            j - 1
        ]["close"]

        current = candles[
            j
        ]["close"]

        if old <= 0:
            continue

        values.append(
            (current - old)
            / old
            * 100.0
        )

    if len(values) < 2:
        return 0.0

    m = np.mean(values)

    return float(
        np.sqrt(
            np.mean(
                (np.asarray(values) - m) ** 2
            )
        )
    )


def ema(candles, i, period):

    alpha = 2.0 / (
        period + 1
    )

    start = max(
        0,
        i - period * 4,
    )

    value = candles[
        start
    ]["close"]

    for j in range(
        start + 1,
        i + 1,
    ):

        value = (
            alpha
            * candles[j]["close"]
            + (1 - alpha)
            * value
        )

    return value


def build_features(candles, i):

    close = candles[
        i
    ]["close"]

    open_price = candles[
        i
    ]["open"]

    high = candles[
        i
    ]["high"]

    low = candles[
        i
    ]["low"]

    volume = candles[
        i
    ]["volume"]

    e20 = ema(
        candles,
        i,
        20,
    )

    e50 = ema(
        candles,
        i,
        50,
    )

    if close <= 0:
        return None

    features = [
        safe_return(candles, i, 1),
        safe_return(candles, i, 3),
        safe_return(candles, i, 6),
        safe_return(candles, i, 12),
        safe_return(candles, i, 24),

        volatility(candles, i, 6),
        volatility(candles, i, 12),
        volatility(candles, i, 24),

        (close - e20)
        / e20
        * 100.0,

        (close - e50)
        / e50
        * 100.0,

        (high - low)
        / close
        * 100.0,

        (close - open_price)
        / close
        * 100.0,

        (
            high
            - max(open_price, close)
        )
        / close
        * 100.0,

        (
            min(open_price, close)
            - low
        )
        / close
        * 100.0,
    ]

    volumes = [
        candles[j]["volume"]
        for j in range(
            max(0, i - 24),
            i,
        )
    ]

    avg_volume = (
        np.mean(volumes)
        if volumes
        else volume
    )

    volume_ratio = (
        volume / avg_volume
        if avg_volume > 0
        else 1.0
    )

    features.append(
        math.log(
            max(
                0.1,
                volume_ratio,
            )
        )
    )

    return features


def build_dataset(all_data):

    rows = []

    for symbol, candles in all_data.items():

        for i in range(
            60,
            len(candles)
            - HORIZON
            - 2,
        ):

            features = build_features(
                candles,
                i,
            )

            if features is None:
                continue

            entry_index = i + 1

            exit_index = (
                entry_index
                + HORIZON
                - 1
            )

            entry = candles[
                entry_index
            ]["open"]

            exit_price = candles[
                exit_index
            ]["close"]

            future_return = (
                exit_price - entry
            ) / entry * 100.0

            target = int(
                future_return > 0
            )

            rows.append({
                "time": candles[i]["time"],
                "features": features,
                "target": target,
            })

    rows.sort(
        key=lambda x: x["time"]
    )

    return rows


def fit_scaler(rows):

    X = np.asarray([
        r["features"]
        for r in rows
    ], dtype=float)

    means = np.mean(
        X,
        axis=0,
    )

    stds = np.std(
        X,
        axis=0,
    )

    stds[
        stds < 1e-8
    ] = 1.0

    return means, stds


def transform_matrix(
    rows,
    means,
    stds,
):

    X = np.asarray([
        r["features"]
        for r in rows
    ], dtype=float)

    X = (
        X - means
    ) / stds

    return np.clip(
        X,
        -10,
        10,
    )


def train_logistic(
    X,
    y,
):

    n, p = X.shape

    weights = np.zeros(p)
    bias = 0.0

    for _ in range(EPOCHS):

        scores = (
            X @ weights
            + bias
        )

        predictions = sigmoid(
            scores
        )

        errors = (
            predictions - y
        )

        gradients = (
            X.T @ errors
        ) / n

        gradients += (
            L2 * weights
        )

        bias_gradient = np.mean(
            errors
        )

        weights -= (
            LEARNING_RATE
            * gradients
        )

        bias -= (
            LEARNING_RATE
            * bias_gradient
        )

    return weights, bias


def predict(
    X,
    weights,
    bias,
):

    return sigmoid(
        X @ weights
        + bias
    )


def fast_auc(
    scores,
    y,
):

    scores = np.asarray(
        scores
    )

    y = np.asarray(y)

    order = np.argsort(
        scores,
        kind="mergesort",
    )

    sorted_scores = scores[
        order
    ]

    sorted_y = y[
        order
    ]

    n_pos = np.sum(
        sorted_y == 1
    )

    n_neg = np.sum(
        sorted_y == 0
    )

    if (
        n_pos == 0
        or n_neg == 0
    ):
        return 0.5

    ranks = np.arange(
        1,
        len(sorted_y) + 1,
        dtype=float,
    )

    rank_sum = np.sum(
        ranks[
            sorted_y == 1
        ]
    )

    return float(
        (
            rank_sum
            - n_pos
            * (n_pos + 1)
            / 2
        )
        / (
            n_pos * n_neg
        )
    )


def prepare_folds(rows):

    n = len(rows)

    fold_size = (
        n // N_FOLDS
    )

    folds = []

    for fold in range(
        N_FOLDS
    ):

        train_end = (
            fold * fold_size
        )

        test_end = (
            (fold + 1)
            * fold_size
        )

        if fold == 0:

            train_end = max(
                MIN_TRAIN,
                fold_size,
            )

        if test_end > n:
            test_end = n

        if (
            train_end >= test_end
        ):
            continue

        train_rows = rows[
            :train_end
        ]

        test_rows = rows[
            train_end:test_end
        ]

        if len(
            train_rows
        ) < MIN_TRAIN:
            continue

        means, stds = fit_scaler(
            train_rows
        )

        X_train = transform_matrix(
            train_rows,
            means,
            stds,
        )

        y_train = np.asarray([
            r["target"]
            for r in train_rows
        ])

        X_test = transform_matrix(
            test_rows,
            means,
            stds,
        )

        y_test = np.asarray([
            r["target"]
            for r in test_rows
        ])

        folds.append({
            "X_train": X_train,
            "y_train": y_train,
            "X_test": X_test,
            "y_test": y_test,
        })

    return folds


def run_real(folds):

    scores_all = []
    targets_all = []

    print()
    print(
        "REAL OOS"
    )

    for i, fold in enumerate(
        folds,
        1,
    ):

        weights, bias = (
            train_logistic(
                fold["X_train"],
                fold["y_train"],
            )
        )

        scores = predict(
            fold["X_test"],
            weights,
            bias,
        )

        auc = fast_auc(
            scores,
            fold["y_test"],
        )

        print(
            f"FOLD {i}: "
            f"AUC={auc:.6f}"
        )

        scores_all.append(
            scores
        )

        targets_all.append(
            fold["y_test"]
        )

    return fast_auc(
        np.concatenate(
            scores_all
        ),
        np.concatenate(
            targets_all
        ),
    )


def run_permutations(folds):

    rng = np.random.default_rng(
        SEED
    )

    results = []

    print()
    print(
        "V44 FAST PERMUTATION TEST"
    )

    for p in range(
        N_PERMUTATIONS
    ):

        scores_all = []
        targets_all = []

        for fold in folds:

            y_perm = (
                fold["y_train"]
                .copy()
            )

            rng.shuffle(
                y_perm
            )

            weights, bias = (
                train_logistic(
                    fold["X_train"],
                    y_perm,
                )
            )

            scores = predict(
                fold["X_test"],
                weights,
                bias,
            )

            scores_all.append(
                scores
            )

            targets_all.append(
                fold["y_test"]
            )

        auc = fast_auc(
            np.concatenate(
                scores_all
            ),
            np.concatenate(
                targets_all
            ),
        )

        results.append(
            auc
        )

        if (
            (p + 1) % 10 == 0
        ):

            print(
                f"Permutation "
                f"{p + 1}/"
                f"{N_PERMUTATIONS} | "
                f"AUC={auc:.6f}"
            )

    return np.asarray(
        results
    )


def main():

    print()
    print("=" * 80)
    print(
        "ALPHAAI V44"
    )
    print(
        "1000 OOS PERMUTATIONS"
    )
    print("=" * 80)

    all_data = {}

    for symbol in SYMBOLS:

        print(
            "DOWNLOAD:",
            symbol,
        )

        candles = (
            download_history(
                symbol
            )
        )

        print(
            "Candles:",
            len(candles),
        )

        if len(candles) >= 1000:

            all_data[
                symbol
            ] = candles

        time.sleep(0.10)

    print()
    print(
        "BUILD DATASET..."
    )

    rows = build_dataset(
        all_data
    )

    print(
        "Observations:",
        len(rows),
    )

    folds = prepare_folds(
        rows
    )

    print(
        "Valid folds:",
        len(folds),
    )

    real_auc = run_real(
        folds
    )

    print()
    print(
        "REAL OOS AUC:",
        f"{real_auc:.6f}",
    )

    permutation_aucs = (
        run_permutations(
            folds
        )
    )

    mean_perm = float(
        np.mean(
            permutation_aucs
        )
    )

    std_perm = float(
        np.std(
            permutation_aucs,
            ddof=1,
        )
    )

    p50 = float(
        np.percentile(
            permutation_aucs,
            50,
        )
    )

    p90 = float(
        np.percentile(
            permutation_aucs,
            90,
        )
    )

    p95 = float(
        np.percentile(
            permutation_aucs,
            95,
        )
    )

    p99 = float(
        np.percentile(
            permutation_aucs,
            99,
        )
    )

    p995 = float(
        np.percentile(
            permutation_aucs,
            99.5,
        )
    )

    p999 = float(
        np.percentile(
            permutation_aucs,
            99.9,
        )
    )

    count_ge = int(
        np.sum(
            permutation_aucs
            >= real_auc
        )
    )

    p_value = (
        count_ge + 1
    ) / (
        N_PERMUTATIONS + 1
    )

    z_score = (
        (
            real_auc
            - mean_perm
        )
        / std_perm
        if std_perm > 0
        else 0.0
    )

    print()
    print("=" * 80)
    print(
        "V44 PERMUTATION SUMMARY"
    )
    print("=" * 80)

    print(
        "Real AUC:",
        f"{real_auc:.6f}",
    )

    print(
        "Permutation mean:",
        f"{mean_perm:.6f}",
    )

    print(
        "Permutation median:",
        f"{p50:.6f}",
    )

    print(
        "Permutation P90:",
        f"{p90:.6f}",
    )

    print(
        "Permutation P95:",
        f"{p95:.6f}",
    )

    print(
        "Permutation P99:",
        f"{p99:.6f}",
    )

    print(
        "Permutation P99.5:",
        f"{p995:.6f}",
    )

    print(
        "Permutation P99.9:",
        f"{p999:.6f}",
    )

    print(
        "Permutation std:",
        f"{std_perm:.6f}",
    )

    print(
        "Z-score:",
        f"{z_score:.3f}",
    )

    print(
        "Empirical p-value:",
        f"{p_value:.5f}",
    )

    print(
        "N permutations:",
        N_PERMUTATIONS,
    )

    print()
    print(
        "VERDETTO V44"
    )

    if p_value < 0.01:

        print(
            "RESULT: EVIDENZA STATISTICA FORTE"
        )

    elif p_value < 0.05:

        print(
            "RESULT: EVIDENZA STATISTICA INTERESSANTE"
        )

    elif p_value < 0.10:

        print(
            "RESULT: EVIDENZA DEBOLE"
        )

    else:

        print(
            "RESULT: COMPATIBILE CON IL RUMORE"
        )

    print()
    print(
        "NON USARE LIVE."
    )


if __name__ == "__main__":
    main()
