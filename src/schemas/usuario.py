from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, validator
import re

class UsuarioBase(BaseModel):
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

    @validator("nombres", "apellidos")
    def validar_texto(cls, v):
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", v):
            raise ValueError("El campo solo puede contener letras y espacios.")
        return v.strip()

    @validator("usuario")
    def validar_usuario(cls, v):
        if not re.match(r"^[A-Za-z0-9]{1,10}$", v):
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

    @validator("rol")
    def validar_rol(cls, v):
        if v not in ("Admin", "Empleado"):
            raise ValueError("El rol debe ser 'Admin' o 'Empleado'.")
        return v


# 👇 Aquí está el cambio importante 👇
class UsuarioCreate(UsuarioBase):
    password: Annotated[str, Field(min_length=8, max_length=30, strip_whitespace=True)]


class UsuarioUpdate(BaseModel):
    nombres: str | None = None
    apellidos: str | None = None
    usuario: str | None = None
    celular: str | None = None
    dni: str | None = None
    rol: str | None = None
    actualizado_por: str | None = None


class UsuarioOut(UsuarioBase):
    id: str

    class Config:
        from_attributes = True  # reemplaza orm_mode en Pydantic v2
