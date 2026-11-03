import numpy as np
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/calcul")
def calcul(n: int = Query(500, ge=1, le=2000)):
    a = np.random.rand(n, n)
    b = np.random.rand(n, n)
    c = a @ b
    return {
        "taille": n,
        "moyenne": float(c.mean()),
        "max": float(c.max()),
        "trace": float(np.trace(c)),
    }