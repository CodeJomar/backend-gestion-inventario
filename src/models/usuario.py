from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id: str
    email: EmailStr
    nombres: str
    apellidos: str
    usuario: str
    celular: Optional[str] = None
    dni: Optional[str] = None
    role_id: str 
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None
    eliminado_por: Optional[str] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    eliminado_en: Optional[datetime] = None
    modified_at: Optional[datetime] = None
