from fastapi import APIRouter

router = APIRouter(prefix="/procesos", tags=["Procesos"])

@router.get("/")
def listar_procesos():
    return {"msg": "Listado de procesos"}
