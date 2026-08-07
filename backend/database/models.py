from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(
        Integer,
        primary_key=True
    )

    symbol = Column(
        String
    )

    price = Column(
        Float
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class AIDecision(Base):
    __tablename__ = "ai_decisions"

    id = Column(
        Integer,
        primary_key=True
    )

    symbol = Column(
        String
    )

    decision = Column(
        String
    )

    score = Column(
        Integer
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Position(Base):
    __tablename__ = "positions"

    id = Column(
        Integer,
        primary_key=True
    )

    symbol = Column(
        String
    )

    entry_price = Column(
        Float
    )

    amount = Column(
        Float
    )

    capital_used = Column(
        Float
    )

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Account(Base):
    __tablename__ = "account"

    id = Column(
        Integer,
        primary_key=True
    )

    balance = Column(
        Float
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(
        Integer,
        primary_key=True
    )

    symbol = Column(
        String
    )

    action = Column(
        String
    )

    entry_price = Column(
        Float
    )

    exit_price = Column(
        Float
    )

    amount = Column(
        Float
    )

    capital_used = Column(
        Float
    )

    profit = Column(
        Float
    )

    reason = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )