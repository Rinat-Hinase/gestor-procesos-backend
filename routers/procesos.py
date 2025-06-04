from fastapi import APIRouter
from pymongo import MongoClient
from models.proceso_model import ProcesoInsert, ProcesoUpdate
from database.proceso_dao import ProcesoDAO
import os
from bson import ObjectId
from typing import Optional
from fastapi import HTTPException
from datetime import datetime

router = APIRouter(prefix="/procesos", tags=["Procesos"])
client = MongoClient(os.getenv("MONGO_URI"))
db = client["GestorProcesos"]
dao = ProcesoDAO(db)

@router.post("/crear")
def crear_proceso(data: ProcesoInsert):
    try:
        proceso = dao.crear_proceso(data)
        return {"mensaje": "Proceso creado correctamente", "id": str(proceso.inserted_id)}

    except Exception as e:
        return {"error": str(e)}
@router.get("/listar")
def listar_procesos():
    try:
        resultados = list(dao.db.find())
        for r in resultados:
            r["_id"] = str(r["_id"])  # Convertir ObjectId
        return resultados
    except Exception as e:
        return {"error": str(e)}
@router.get("/{id}")
def obtener_proceso(id: str):
    try:
        proceso = dao.db.find_one({"_id": ObjectId(id)})
        if not proceso:
            return {"error": "Proceso no encontrado"}
        proceso["_id"] = str(proceso["_id"])  # Convertir ObjectId a str
        return proceso
    except Exception as e:
        return {"error": str(e)}

@router.patch("/{id}")
def actualizar_proceso(id: str, datos: ProcesoUpdate):
    try:
        cambios = {k: v for k, v in datos.dict().items() if v is not None}

        # 🔁 Convertir fecha_inicio y fecha_fin si existen
        if "fecha_inicio" in cambios:
            cambios["fecha_inicio"] = datetime.combine(cambios["fecha_inicio"], datetime.min.time())
        if "fecha_fin" in cambios:
            cambios["fecha_fin"] = datetime.combine(cambios["fecha_fin"], datetime.min.time())

        if not cambios:
            return {"mensaje": "No se enviaron cambios"}

        resultado = dao.db.update_one({"_id": ObjectId(id)}, {"$set": cambios})
        if resultado.matched_count == 0:
            return {"error": "Proceso no encontrado"}
        return {"mensaje": "Proceso actualizado"}
    except Exception as e:
        return {"error": str(e)}
@router.delete("/{id}")
def eliminar_proceso(id: str):
    try:
        resultado = dao.db.delete_one({"_id": ObjectId(id)})
        if resultado.deleted_count == 0:
            return {"error": "Proceso no encontrado"}
        return {"mensaje": "Proceso eliminado correctamente"}
    except Exception as e:
        return {"error": str(e)}


