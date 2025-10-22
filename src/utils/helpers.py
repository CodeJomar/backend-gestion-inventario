# src/utils/helpers.py
from decimal import Decimal

def _to_int(value, name="valor"):
    """Convierte seguros a int (acepta int, str con dígitos, Decimal)."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, Decimal):
        return int(value)
    if isinstance(value, str):
        try:
            # permitir "35" o "35.0"
            if "." in value:
                return int(float(value))
            return int(value)
        except Exception:
            raise ValueError(f"{name} no es un número válido: {value!r}")
    raise ValueError(f"{name} tiene un tipo no soportado: {type(value)}")

def calcular_nuevo_stock(stock_actual, cantidad, tipo_movimiento: str) -> int:
    """Calcula el nuevo stock después de una entrada o salida.
    Normaliza tipos y valida resultados.
    """
    stock_actual = _to_int(stock_actual, "stock_actual")
    cantidad = _to_int(cantidad, "cantidad")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0.")

    if tipo_movimiento == "entrada":
        return stock_actual + cantidad
    elif tipo_movimiento == "salida":
        nuevo_stock = stock_actual - cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay suficiente stock para realizar la salida.")
        return nuevo_stock
    else:
        raise ValueError("Tipo de movimiento inválido.")
