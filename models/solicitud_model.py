from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class SolicitudInsert(BaseModel):
    descripcion: str
    tipo_area: str
    responsable_seguimiento: str
    fecha_estimacion: date
    documentos_url: Optional[List[str]] = []  # <-- Ya está bien aquí

class SolicitudUpdate(BaseModel):
    estatus: Optional[str] = None
    retroalimentacion: Optional[str] = None
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por: Optional[str] = None
    documentos_url: Optional[List[str]] = None  # <-- AGREGA ESTA LÍNEA
