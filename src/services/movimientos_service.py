# src/services/movimientos_service.py
from fastapi import HTTPException
from datetime import datetime
from src.db.repositories import movimientos_repository, productos_repository
from src.utils.helpers import calcular_nuevo_stock

def listar_movimientos():
    return movimientos_repository.listar_movimientos()

def crear_movimiento(data: dict):
    producto_id = data.get("producto_id")
    tipo_movimiento = data.get("tipo_movimiento")
    cantidad = data.get("cantidad")

    # validaciones básicas previas
    if not producto_id:
        raise HTTPException(status_code=400, detail="producto_id es requerido")
    if not tipo_movimiento:
        raise HTTPException(status_code=400, detail="tipo_movimiento es requerido")
    if cantidad is None:
        raise HTTPException(status_code=400, detail="cantidad es requerida")

    # Verificar si el producto existe
    producto = productos_repository.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Asegurar valor de stock actual (normaliza tipos)
    stock_actual = producto.get("stock", 0)

    # Calcular nuevo stock (calcular_nuevo_stock ahora normaliza tipos)
    try:
        nuevo_stock = calcular_nuevo_stock(stock_actual, cantidad, tipo_movimiento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Actualizar producto en BD
    productos_repository.actualizar_producto(producto_id, {"stock": nuevo_stock})

    # Preparar datos del movimiento: rellenar fecha y campos derivados si faltan
    fecha = data.get("fecha") or datetime.utcnow()
    if isinstance(fecha, str):
        try:
            fecha = datetime.fromisoformat(fecha)
        except Exception:
            fecha = datetime.utcnow()
    data["fecha"] = fecha

    # Registrar movimiento (repositorio serializa datetimes)
    movimiento = movimientos_repository.crear_movimiento(data)

    return {
        "mensaje": "Movimiento registrado correctamente",
        "nuevo_stock": nuevo_stock,
        "movimiento": movimiento
    }
