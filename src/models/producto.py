from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Producto:
    sku: str
    id: str
    nombre: str
    marca: str
    categoria: str # cocina, cuidado del hogar, cuidado personal, tecnología.
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    tipo: str = "electrodomestico"  # electrodomestico, accesorio, consumible
    imagen_url: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None
    modified_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    modified_at: datetime
    estado: bool = True  # True: activo, False: inactivo
