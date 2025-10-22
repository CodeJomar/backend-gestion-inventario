from fastapi import HTTPException
from src.db.repositories import movimientos_repository, productos_repository
from src.utils.helpers import calcular_nuevo_stock

def listar_movimientos():
    return movimientos_repository.listar_movimientos()

def crear_movimiento(data: dict):
    producto_id = data.get("producto_id")
    tipo_movimiento = data.get("tipo_movimiento")
    cantidad = data.get("cantidad")

    # Verificar si el producto existe
    producto = productos_repository.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Calcular nuevo stock
    try:
        nuevo_stock = calcular_nuevo_stock(producto["stock"], cantidad, tipo_movimiento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Actualizar producto en BD
    productos_repository.actualizar_producto(producto_id, {"stock": nuevo_stock})

    # Registrar movimiento (ya incluye fecha, día, mes, etc. desde el schema)
    movimiento = movimientos_repository.crear_movimiento(data)

    return {
        "mensaje": "Movimiento registrado correctamente",
        "nuevo_stock": nuevo_stock,
        "movimiento": movimiento
    }
