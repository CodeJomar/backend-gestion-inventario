from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Movimiento:
    id: str
    producto_id: str
    tipo_movimiento: str  # entrada o salida
    cantidad: int
    motivo: str  # venta, devolucion, reposición, ajuste
    create_by: Optional[str] = None
    fecha: datetime
    created_at: datetime
    modified_at: datetime
