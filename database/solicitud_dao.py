from datetime import datetime
from pymongo.collection import Collection
from bson import ObjectId

class SolicitudDAO:
    def __init__(self, db):
        self.db: Collection = db["Solicitudes"]

    def generar_folio(self) -> str:
        total = self.db.count_documents({})
        return f"CCADPRC-{total + 1:04d}"

    def crear_solicitud(self, data):
        folio = self.generar_folio()
        prioridad = clasificar_prioridad(data.descripcion)

        nueva = {
            "descripcion": data.descripcion,
            "tipo_area": data.tipo_area,
            "responsable_seguimiento": data.responsable_seguimiento,
            "fecha_estimacion": datetime.combine(data.fecha_estimacion, datetime.min.time()),
            "fecha_creacion": datetime.now(),
            "estatus": "Pendiente",
            "folio": folio,
            "documentos_url": data.documentos_url or [],
            "prioridad": prioridad
        }
        self.db.insert_one(nueva)
        return folio

def clasificar_prioridad(descripcion: str) -> str:
    desc = descripcion.lower()
    if any(p in desc for p in ["urgente", "inmediato", "auditoría", "cumplimiento", "norma"]):
        return "Alta"
    elif any(p in desc for p in ["mejora", "propuesta", "optimizar", "eficiencia"]):
        return "Media"
    else:
        return "Baja"
