from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    marca: str
    categoria: str
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    descripcion: Optional[str]
    tipo: Optional[str] = "electrodomestico"
    imagen_url: Optional[str]

class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    marca: Optional[str]
    categoria: Optional[str]
    precio: Optional[float]
    stock: Optional[int]
    descripcion: Optional[str]
    imagen_url: Optional[str]

class ProductoOut(ProductoCreate):
    id: str
