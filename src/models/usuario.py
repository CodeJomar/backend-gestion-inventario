from datetime import datetime
from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    id: str
    email: EmailStr
    nombres: str
    apellidos: str
    usuario: str
    celular: str | None = None
    dni: str | None = None
    rol: str
    creado_por: str | None = None
    actualizado_por: str | None = None
    eliminado_por: str | None = None
    creado_en: datetime | None = None
    actualizado_en: datetime | None = None
    eliminado_en: datetime | None = None
