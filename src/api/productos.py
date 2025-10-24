from fastapi import APIRouter
from src.schemas.producto import ProductoCreate, ProductoUpdate
from src.services import productos_service

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
def crear_producto(prod: ProductoCreate):
    data = prod.dict()
    return productos_service.crear_producto(data)

# Actualizar producto existente
@router.put("/{id}")
def actualizar_producto(id: str, prod: ProductoUpdate):
    data = prod.dict(exclude_unset=True)
    return productos_service.actualizar_producto(id, data)

# Eliminar un producto
@router.delete("/{id}")
def eliminar_producto(id: str):
    return productos_service.eliminar_producto(id)
