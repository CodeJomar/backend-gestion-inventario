from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Movimiento:
    id: str
    producto_id: str
    tipo_movimiento: str  # entrada o salida
    cantidad: int
    motivo: Optional[str] # venta, devolucion, reposición, ajuste.
    usuario: Optional[str]
    fecha: datetime
