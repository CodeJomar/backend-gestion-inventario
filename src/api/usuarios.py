from fastapi import APIRouter, Depends
from src.services import usuarios_service
from src.schemas.usuario import UsuarioCreate, UsuarioOut
from src.auth.dependencies import require_admin, get_current_user

router = APIRouter()

@router.get("/", response_model=list[UsuarioOut], dependencies=[Depends(require_admin)])
def listar_usuarios():
    return usuarios_service.listar_usuarios()

@router.get("/{user_id}", response_model=UsuarioOut, dependencies=[Depends(require_admin)])
def obtener_usuario(user_id: str):
    return usuarios_service.obtener_usuario(user_id)

@router.post("/", dependencies=[Depends(require_admin)])
def crear_usuario(perfil: UsuarioCreate, current_user=Depends(get_current_user)):
    perfil_data = perfil.dict()
    perfil_data["creado_por"] = current_user["id"]
    return usuarios_service.crear_usuario(perfil_data)

@router.put("/{user_id}", dependencies=[Depends(require_admin)])
def actualizar_usuario(user_id: str, perfil: UsuarioCreate, current_user=Depends(get_current_user)):
    perfil_data = perfil.dict(exclude_unset=True)
    perfil_data["actualizado_por"] = current_user["id"]
    return usuarios_service.actualizar_usuario(user_id, perfil_data)

@router.delete("/{user_id}", dependencies=[Depends(require_admin)])
def eliminar_usuario(user_id: str, current_user=Depends(get_current_user)):
    return usuarios_service.eliminar_usuario(user_id)
