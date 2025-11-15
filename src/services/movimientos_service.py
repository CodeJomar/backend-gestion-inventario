from fastapi import HTTPException
from datetime import datetime
from src.db.repositories import movimientos_repository, productos_repository
from src.utils.helpers import calcular_nuevo_stock
from fastapi.responses import StreamingResponse
from src.utils.pdf_generator import generar_pdf_movimiento

def listar_movimientos():
    return movimientos_repository.listar_movimientos()

def crear_movimiento(data: dict):
    producto_id = data.get("producto_id")
    tipo_movimiento = data.get("tipo_movimiento")
    cantidad = data.get("cantidad")

    if not producto_id:
        raise HTTPException(status_code=400, detail="producto_id es requerido")
    if not tipo_movimiento:
        raise HTTPException(status_code=400, detail="tipo_movimiento es requerido")
    if cantidad is None:
        raise HTTPException(status_code=400, detail="cantidad es requerida")

    producto = productos_repository.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    stock_actual = producto.get("stock", 0)

    try:
        nuevo_stock = calcular_nuevo_stock(stock_actual, cantidad, tipo_movimiento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    productos_repository.actualizar_producto(producto_id, {"stock": nuevo_stock})

    fecha = data.get("fecha") or datetime.utcnow()
    if isinstance(fecha, str):
        try:
            fecha = datetime.fromisoformat(fecha)
        except Exception:
            fecha = datetime.utcnow()
    data["fecha"] = fecha

    movimiento = movimientos_repository.crear_movimiento(data)

    return {
        "mensaje": "Movimiento registrado correctamente",
        "nuevo_stock": nuevo_stock,
        "movimiento": movimiento
    }

def descargar_pdf_movimiento(movimiento_id: str):
    movimiento = movimientos_repository.obtener_movimiento_por_id(movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    producto = productos_repository.obtener_producto(movimiento["producto_id"])
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    pdf_stream = generar_pdf_movimiento(movimiento, producto)

    filename = f"movimiento_{movimiento_id}.pdf"

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )