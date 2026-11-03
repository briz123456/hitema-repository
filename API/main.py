from fastapi import FastAPI
#from prometheus_fastapi_instrumentator import Instrumentator
import time
 
app = FastAPI()
items = []
 
# Ajoute la collecte des métriques et l'endpoint /metrics
#Instrumentator().instrument(app).expose(app)
 
 
@app.get("/health")
def health():
    return {"status": "ok"}
 
 
@app.get("/items")
def list_items():
    return items
 
 
@app.post("/items")
def add_item(name: str):
    items.append(name)
    return {"added": name}
 
 
@app.get("/slow")  # Pour le jour 4
def slow():
    time.sleep(2)
    return {"slow": True}