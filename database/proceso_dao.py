# database/proceso_dao.py
from models.proceso_model import ProcesoInsert
from datetime import datetime

class ProcesoDAO:
    def __init__(self, db):
        self.db = db["Procesos"]
        self.solicitudes = db["Solicitudes"]

    def crear_proceso(self, data: ProcesoInsert):
      proceso = {
          "solicitud_folio": data.solicitud_folio,
          "descripcion": data.descripcion,
          "responsables": data.responsables,
          "fecha_inicio": datetime.combine(data.fecha_inicio, datetime.min.time()),
          "fecha_fin": datetime.combine(data.fecha_fin, datetime.min.time()),
          "fecha_creacion": datetime.now()
      }
      resultado = self.db.insert_one(proceso)
      return resultado  # 🔄 Retornas el InsertOneResult para usar .inserted_id
