from pydantic import BaseModel, Field
from typing import Optional

class MovimientoCreate(BaseModel):
    producto_id: str
    tipo_movimiento: str
    cantidad: int = Field(..., gt=0)
    motivo: Optional[str]
    usuario: Optional[str]

class MovimientoOut(MovimientoCreate):
    id: str
