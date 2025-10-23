from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Producto:
    id: str
    nombre: str
    marca: str
    categoria: str # cocina, cuidado del hogar, cuidado personal, tecnología.
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    tipo: str = "electrodomestico"  # electrodomestico, accesorio, consumible
    imagen_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    modified_at: datetime
