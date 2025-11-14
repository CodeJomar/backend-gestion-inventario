from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    marca: str
    categoria: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    tipo: Literal["electrodomestico", "accesorio", "consumible"] = "electrodomestico"
    imagen_url: Optional[str] = None

    @validator("tipo")
    def validar_tipo(cls, v):
        if v not in ("electrodomestico", "accesorio", "consumible"):
            raise ValueError("El tipo debe ser 'electrodomestico', 'accesorio' o 'consumible'.")
        return v

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    tipo: Optional[Literal["electrodomestico", "accesorio", "consumible"]] = None
    imagen_url: Optional[str] = None

class ProductoOut(ProductoBase):
    id: str
    created_by: str
    updated_by: str
    modified_by: str
    created_at: datetime
    updated_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
