from fastapi import FastAPI
from src.core.cors import configurar_cors
from src.core.config import settings
from src.api import productos, movimientos, usuarios, auth


app = FastAPI(title=settings.PROJECT_NAME)
configurar_cors(app)

routes = [productos, movimientos, usuarios, auth]
for r in routes:
    app.include_router(r.router)

@app.get("/")
def root():
    return {"mensaje": f"{settings.PROJECT_NAME} funcionando..."}
