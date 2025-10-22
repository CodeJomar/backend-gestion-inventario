from fastapi import APIRouter
from src.schemas.movimiento import MovimientoCreate, MovimientoOut
from src.services import movimientos_service

router = APIRouter()

@router.get("/", response_model=list[MovimientoOut])
def listar_movimientos():
    """Lista todos los movimientos registrados."""
    return movimientos_service.listar_movimientos()

@router.post("/", response_model=dict)
def crear_movimiento(mov: MovimientoCreate):
    """Crea un movimiento y actualiza el stock del producto."""
    return movimientos_service.crear_movimiento(mov.dict())
