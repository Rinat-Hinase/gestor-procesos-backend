from fastapi import APIRouter, UploadFile, File,  Query
from fastapi import Depends
from models.solicitud_model import SolicitudInsert, SolicitudUpdate
from database.solicitud_dao import SolicitudDAO
from utils.supabase_config import subir_archivo
from pymongo import MongoClient
from typing import Optional
from datetime import datetime
from datetime import timedelta
import os

# Router
router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

# Conexión a MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["GestorProcesos"]
dao = SolicitudDAO(db)

@router.post("/subir-documento/")
async def subir_documento(
    file: UploadFile = File(...)
):
    try:
        contents = await file.read()
        url = subir_archivo(contents, file.filename, file.content_type)  # 👈 sin carpeta
        return {"url": url}
    except Exception as e:
        return {"error": str(e)}




# Endpoint: crear nueva solicitud completa
@router.post("/crear")
def crear_solicitud(data: SolicitudInsert):
    try:
        folio = dao.crear_solicitud(data)
        return {"mensaje": "Solicitud creada exitosamente", "folio": folio}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: listar solicitudes
@router.get("/listar")
def listar_solicitudes(
    estatus: Optional[str] = None,
    desde: Optional[str] = None,
    hasta: Optional[str] = None,
):
    try:
        filtro = {}

        if estatus:
            filtro["estatus"] = estatus

        if desde or hasta:
            filtro_fecha = {}
            if desde:
                filtro_fecha["$gte"] = datetime.strptime(desde, "%Y-%m-%d")
            if hasta:
                filtro_fecha["$lte"] = datetime.strptime(hasta, "%Y-%m-%d")
            filtro["fecha_creacion"] = filtro_fecha

        resultados = list(dao.db.find(filtro, {"_id": 0}))
        return resultados

    except Exception as e:
        return {"error": str(e)}

@router.patch("/{folio}")
def actualizar_solicitud(folio: str, data: SolicitudUpdate):
    try:
        cambios = {k: v for k, v in data.dict().items() if v is not None}
        print("📦 Cambios recibidos en PATCH:", cambios)

        if not cambios:
            return {"mensaje": "No se enviaron campos para actualizar."}

        # Validación para evitar finalizar sin aprobación
        if cambios.get("estatus") == "Finalizado":
            solicitud_actual = dao.db.find_one({"folio": folio})
            if not solicitud_actual:
                return {"error": "Solicitud no encontrada"}

            aprobado_por = solicitud_actual.get("aprobado_por")
            fecha_aprobacion = solicitud_actual.get("fecha_aprobacion")

            if not aprobado_por or not fecha_aprobacion:
                return {"error": "No puedes finalizar una solicitud que no ha sido aprobada"}

        resultado = dao.db.update_one({"folio": folio}, {"$set": cambios})
        if resultado.matched_count == 0:
            return {"mensaje": f"No se encontró solicitud con folio {folio}"}
        return {"mensaje": f"Solicitud {folio} actualizada correctamente"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/verificar-evaluaciones-expiradas")
def verificar_solicitudes_expiradas():
    try:
        hoy = datetime.utcnow()

        solicitudes = list(dao.db.find({"estatus": "Pendiente"}))
        actualizadas = 0

        for s in solicitudes:
            fecha_creacion = s.get("fecha_creacion")
            if not fecha_creacion:
                continue

            dias_transcurridos = (hoy - fecha_creacion).days

            if dias_transcurridos >= 3:
                dao.db.update_one(
                    {"folio": s["folio"]},
                    {"$set": {"estatus": "Pendiente Evaluación"}}
                )
                actualizadas += 1

        return {
            "mensaje": f"Se actualizaron {actualizadas} solicitud(es) a 'Pendiente Evaluación'"
        }
    except Exception as e:
        return {"error": str(e)}