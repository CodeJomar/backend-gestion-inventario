from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Producto:
    id: str
    nombre: str
    marca: str
    categoria: str # cocina, cuidado del hogar, cuidado personal, tecnología.
    descripcion: Optional[str]
    precio: float
    stock: int
    tipo: str  # electrodomestico, accesorio, consumible
    imagen_url: Optional[str]
    created_at: datetime
    updated_at: datetime
