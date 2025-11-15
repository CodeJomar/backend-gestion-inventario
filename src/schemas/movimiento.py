from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

class MovimientoBase(BaseModel):
    producto_id: str
    tipo_movimiento: Literal["entrada", "salida"]
    cantidad: int = Field(..., gt=0, description="Cantidad debe ser mayor a 0")
    motivo: Literal["venta", "devolución", "reposición", "ajuste"]
    created_by: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.now)

    @validator("tipo_movimiento")
    def validar_tipo_movimiento(cls, v):
        if v not in ("entrada", "salida"):
            raise ValueError("El tipo_movimiento debe ser 'entrada' o 'salida'.")
        return v

    @validator("motivo")
    def validar_motivo(cls, v, values):
        tipo = values.get("tipo_movimiento")
        motivos_validos = ("venta", "devolución", "reposición", "ajuste")
        if v not in motivos_validos:
            raise ValueError(f"Motivo inválido. Debe ser uno de: {motivos_validos}")
        if v == "venta" and tipo != "salida":
            raise ValueError("El motivo 'venta' solo es válido para tipo_movimiento 'salida'.")
        if v in ("devolución", "reposición") and tipo != "entrada":
            raise ValueError(f"El motivo '{v}' solo es válido para tipo_movimiento 'entrada'.")
        return v

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoUpdate(BaseModel):
    producto_id: Optional[str] = None
    tipo_movimiento: Optional[Literal["entrada", "salida"]] = None
    cantidad: Optional[int] = Field(None, gt=0)
    motivo: Optional[Literal["venta", "devolución", "reposición", "ajuste"]] = None
    created_by: Optional[str] = None
    fecha: Optional[datetime] = None

class MovimientoOut(MovimientoBase):
    id: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
