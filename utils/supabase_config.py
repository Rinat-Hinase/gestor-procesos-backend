import io
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
import random

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "documentos"

def subir_archivo(contenido: bytes, nombre_archivo: str, tipo: str = "application/octet-stream", carpeta: str = "") -> str:
    # 🕒 Sufijo timestamp + aleatorio para evitar duplicados
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    aleatorio = random.randint(1000, 9999)
    nombre_base, extension = os.path.splitext(nombre_archivo)
    nuevo_nombre = f"{nombre_base}_{timestamp}_{aleatorio}{extension}"

    path = f"{carpeta}/{nuevo_nombre}" if carpeta else nuevo_nombre

    tipo = tipo or "application/octet-stream"

    res = supabase.storage.from_(BUCKET).upload(
        path=path,
        file=contenido,
        file_options={"content-type": tipo}
    )

    if hasattr(res, "error") and res.error:
        raise Exception(f"Supabase error: {res.error.message}")

    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{path}"

