def calcular_nuevo_stock(stock_actual: int, cantidad: int, tipo_movimiento: str) -> int:
    """Calcula el nuevo stock después de una entrada o salida."""
    if tipo_movimiento == "entrada":
        return stock_actual + cantidad
    elif tipo_movimiento == "salida":
        nuevo_stock = stock_actual - cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay suficiente stock para realizar la salida.")
        return nuevo_stock
    else:
        raise ValueError("Tipo de movimiento inválido.")


def formatear_moneda(valor: float, simbolo: str = "S/") -> str:
    """Devuelve el valor en formato monetario."""
    return f"{simbolo} {valor:,.2f}"
