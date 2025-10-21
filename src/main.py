from fastapi import FastAPI
from src.core.cors import configurar_cors
from src.core.config import settings
from src.api import productos

app = FastAPI(title=settings.PROJECT_NAME)
configurar_cors(app)
app.include_router(productos.router, prefix="/productos", tags=["Productos"])

@app.get("/")
def root():
    return {"mensaje": f"{settings.PROJECT_NAME} funcionando..."}
