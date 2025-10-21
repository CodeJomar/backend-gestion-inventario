from src.db.repositories import productos_repository
from fastapi import HTTPException

def listar_productos():
    productos = productos_repository.listar_productos()
    return productos

def obtener_producto(id: str):
    producto = productos_repository.obtener_producto(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

def crear_producto(data: dict):
    nuevo = productos_repository.crear_producto(data)
    return nuevo

def actualizar_producto(id: str, data: dict):
    existente = productos_repository.obtener_producto(id)
    if not existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    actualizado = productos_repository.actualizar_producto(id, data)
    return actualizado

def eliminar_producto(id: str):
    existente = productos_repository.obtener_producto(id)
    if not existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    productos_repository.eliminar_producto(id)
    return {"mensaje": "Producto eliminado correctamente"}
