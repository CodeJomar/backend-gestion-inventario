from fastapi import APIRouter, Depends, HTTPException
from core.auth import CurrentUser, require_roles
from src.schemas.usuario import UsuarioCreate, UsuarioUpdate
from src.services import usuarios_service

router = APIRouter()

@router.post("/")
def crear_usuario(usuario: UsuarioCreate, current_user: CurrentUser = Depends(require_roles("Admin"))):
    try:
        nuevo_usuario = usuarios_service.crear_usuario(usuario.dict())
        return nuevo_usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def listar_usuarios():
    try:
        return usuarios_service.listar_usuarios()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: str):
    usuario = usuarios_service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: str, usuario: UsuarioUpdate):
    try:
        actualizado = usuarios_service.actualizar_usuario(usuario_id, usuario.dict(exclude_unset=True))
        return {"mensaje": "Usuario actualizado correctamente", "usuario": actualizado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: str):
    try:
        return usuarios_service.eliminar_usuario(usuario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
