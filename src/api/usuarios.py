import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from src.core.auth import CurrentUser, require_roles, get_current_user
from src.schemas.usuario import UsuarioCreate, UsuarioUpdate
from src.services import usuarios_service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/")
def crear_usuario(usuario: UsuarioCreate, current_user: CurrentUser = Depends(require_roles("Admin"))):
    try:
        nuevo_usuario = usuarios_service.crear_usuario(usuario, creado_por=current_user.id)
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
def actualizar_usuario(usuario_id: str, usuario: UsuarioUpdate, current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role_name != "Admin" and current_user.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not match the user id.")
    try:
        data = usuario.dict(exclude_unset=True)
        dni = data.pop('dni', None)
        if dni:
            data['dni'] = str(dni)
        if current_user.role_name != "Admin" or current_user.id == usuario_id:
            data.pop("active", None)
            data.pop("rol", None)
        if not data:
            error = "Algo salio mal."
            if current_user.role_name != "Admin":
                error = "Solo un administrador puede cambiar el estado de activo."
            if current_user.id == usuario_id:
                error = "No puedes cambiar el estado de activo de tu mismo usuario."
            raise HTTPException(status_code=400, detail=error)
        actualizado = usuarios_service.actualizar_usuario(usuario_id, data, current_user.id)
        return {"mensaje": "Usuario actualizado correctamente", "usuario": actualizado}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(e, flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: str):
    try:
        return usuarios_service.eliminar_usuario(usuario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
