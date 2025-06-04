# models/proceso_model.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProcesoInsert(BaseModel):
    solicitud_folio: str
    descripcion: str
    responsables: List[str]
    fecha_inicio: date
    fecha_fin: date
class ProcesoUpdate(BaseModel):
    descripcion: Optional[str] = None
    responsables: Optional[List[str]] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None