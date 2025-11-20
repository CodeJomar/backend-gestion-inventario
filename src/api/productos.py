from fastapi import APIRouter, Depends
from datetime import datetime
from src.schemas.producto import ProductoCreate, ProductoUpdate
from src.services import productos_service
from src.core.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/productos", tags=["Productos"])

# Listar todos los productos
@router.get("/")
def listar_productos():
    return productos_service.listar_productos()

# Obtener un producto por ID
@router.get("/{id}")
def obtener_producto(id: str):
    return productos_service.obtener_producto(id)

# Crear un nuevo producto
@router.post("/")
def crear_producto(prod: ProductoCreate, current_user: CurrentUser = Depends(get_current_user)):
    data = prod.dict()
    # Registrar quién creó el producto
    data["created_by"] = current_user.email
    return productos_service.crear_producto(data)

# Actualizar producto existente
@router.put("/{id}")
def actualizar_producto(id: str, prod: ProductoUpdate, current_user: CurrentUser = Depends(get_current_user)):
    data = prod.dict(exclude_unset=True)
    # Registrar quién realizó la modificación
    data["modified_by"] = current_user.email
    data["modified_at"] = datetime.utcnow().isoformat()
    return productos_service.actualizar_producto(id, data)

# Desactivar un producto
@router.put("/{id}/desactivar")
def desactivar_producto(id: str, current_user: CurrentUser = Depends(get_current_user)):
    # Usar la ruta de actualización para fijar quien desactiva
    data = {"estado": False, "modified_by": current_user.email, "modified_at": datetime.utcnow().isoformat()}
    return productos_service.actualizar_producto(id, data)

# Activar un producto
@router.put("/{id}/activar")
def activar_producto(id: str, current_user: CurrentUser = Depends(get_current_user)):
    data = {"estado": True, "modified_by": current_user.email, "modified_at": datetime.utcnow().isoformat()}
    return productos_service.actualizar_producto(id, data)
