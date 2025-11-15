from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.services import reportes_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/productos/activos")
def reporte_productos_activos():
    stream = reportes_service.generar_excel_productos_activos()
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=productos_activos.xlsx"}
    )


@router.get("/productos/inactivos")
def reporte_productos_inactivos():
    stream = reportes_service.generar_excel_productos_inactivos()
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=productos_inactivos.xlsx"}
    )


@router.get("/movimientos/entrada")
def reporte_movimientos_entrada():
    stream = reportes_service.generar_excel_movimientos_entrada()
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=movimientos_entrada.xlsx"}
    )


@router.get("/movimientos/salida")
def reporte_movimientos_salida():
    stream = reportes_service.generar_excel_movimientos_salida()
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=movimientos_salida.xlsx"}
    )
