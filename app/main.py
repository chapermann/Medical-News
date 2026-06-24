from fastapi import FastAPI
from app.api import engines

app = FastAPI(title="Medical News")

app.include_router(engines.router)

@app.get("/")
def root():
    return {"status": "Medical News running"}
