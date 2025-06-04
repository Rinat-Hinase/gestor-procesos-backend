from fastapi import FastAPI
from routers import solicitudes, procesos
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(solicitudes.router)
app.include_router(procesos.router)

@app.get("/")
def read_root():
    return {"message": "Gestor de Procesos API"}
