from fastapi import FastAPI
from routers import solicitudes, procesos

app = FastAPI()

app.include_router(solicitudes.router)
app.include_router(procesos.router)

@app.get("/")
def read_root():
    return {"message": "Gestor de Procesos API"}
