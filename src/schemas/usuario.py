from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nombres: str
    apellidos: str
    usuario: str
    celular: Optional[str] = None
    dni: Optional[str] = None
    rol: Optional[str] = None
    role_id: Optional[str] = None
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None
    eliminado_por: Optional[str] = None

    @validator("nombres", "apellidos")
    def validar_texto(cls, v):
        if v and not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", v):
            raise ValueError("El campo solo puede contener letras y espacios.")
        return v.strip() if v else v

    @validator("usuario")
    def validar_usuario(cls, v):
        if v and not re.match(r"^[A-Za-z0-9]{1,10}$", v):
            raise ValueError("El usuario debe tener máximo 10 caracteres, sin espacios ni símbolos.")
        return v

    @validator("celular")
    def validar_celular(cls, v):
        if v and not re.match(r"^9\d{8}$", v):
            raise ValueError("El celular debe tener formato peruano (9XXXXXXXX).")
        return v

    @validator("dni")
    def validar_dni(cls, v):
        if v and not re.match(r"^\d{8}$", v):
            raise ValueError("El DNI debe tener 8 dígitos.")
        return v

class UsuarioCreate(UsuarioBase):
    password: Annotated[str, Field(min_length=8, max_length=30, strip_whitespace=True)]

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    usuario: Optional[str] = None
    celular: Optional[str] = None
    dni: Optional[str] = None
    rol: Optional[str] = None
    role_id: Optional[str] = None
    actualizado_por: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: str
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    eliminado_en: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True
