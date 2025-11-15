from fastapi import APIRouter, Depends
from src.schemas.movimiento import MovimientoCreate, MovimientoOut
from src.services import movimientos_service
from src.core.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])

@router.get("/", response_model=list[MovimientoOut])
def listar_movimientos():
    """Lista todos los movimientos registrados."""
    return movimientos_service.listar_movimientos()

@router.post("/", response_model=dict)
def crear_movimiento(mov: MovimientoCreate, current_user: CurrentUser = Depends(get_current_user)):
    """Crea un movimiento y actualiza el stock del producto."""
    data = mov.dict()
    data["created_by"] = current_user.email
    return movimientos_service.crear_movimiento(data)
