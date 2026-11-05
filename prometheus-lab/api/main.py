import asyncio
import random

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="API monitorée")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/slow")
async def slow():
    # Latence aléatoire pour avoir un histogramme intéressant
    await asyncio.sleep(random.uniform(0.1, 0.8))
    return {"status": "slow"}


@app.get("/error")
def error():
    # 30 % d'erreurs 500 pour tester les métriques par status
    if random.random() < 0.3:
        raise HTTPException(status_code=500, detail="boom")
    return {"status": "ok"}


# Instrumente toutes les routes et expose /metrics
Instrumentator().instrument(app).expose(app)
