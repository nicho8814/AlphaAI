from fastapi import FastAPI

app = FastAPI(
    title="AlphaAI",
    version="0.1"
)


@app.get("/")
def home():
    return {
        "status": "AlphaAI online",
        "version": "0.1"
    }
