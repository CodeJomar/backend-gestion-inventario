from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

class MovimientoBase(BaseModel):
    producto_id: str
    tipo_movimiento: Literal["entrada", "salida"]
    cantidad: int = Field(..., gt=0, description="Cantidad debe ser mayor a 0")
    motivo: Literal["venta", "devolución", "reposición", "ajuste"]
    usuario: Optional[str] = Field(None, description="Usuario que realiza el movimiento")
    fecha: datetime = Field(default_factory=datetime.now)

    # Campos derivados
    dia: Optional[int] = None
    mes: Optional[int] = None
    anio: Optional[int] = None
    hora: Optional[str] = None

    @validator("motivo")
    def validar_motivo_tipo_movimiento(cls, v, values):
        """Valida coherencia entre motivo y tipo_movimiento."""
        tipo = values.get("tipo_movimiento")

        # Reglas de coherencia
        if v == "venta" and tipo != "salida":
            raise ValueError("El motivo 'venta' solo es válido para tipo_movimiento 'salida'.")
        if v in ("devolución", "reposición", "ajuste") and tipo != "entrada":
            raise ValueError(f"El motivo '{v}' solo es válido para tipo_movimiento 'entrada'.")
        return v

    @validator("fecha", pre=True, always=True)
    def establecer_fecha_y_derivados(cls, v, values):
        """Genera automáticamente fecha, día, mes, año y hora."""
        dt = v or datetime.now()
        values["dia"] = dt.day
        values["mes"] = dt.month
        values["anio"] = dt.year
        values["hora"] = dt.strftime("%H:%M:%S")
        return dt


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoOut(MovimientoBase):
    id: str

    class Config:
        orm_mode = True
