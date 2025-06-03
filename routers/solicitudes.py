from fastapi import APIRouter

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

@router.get("/")
def listar_solicitudes():
    return {"msg": "Listado de solicitudes"}

@router.post("/")
def crear_solicitud():
    return {"msg": "Solicitud creada"}
