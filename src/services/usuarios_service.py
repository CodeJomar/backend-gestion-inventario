from src.db.repositories import usuarios_repository
from src.auth.auth_service import registrar_usuario
from fastapi import HTTPException

def listar_usuarios():
    return usuarios_repository.obtener_usuarios()

def obtener_usuario(user_id: str):
    usuario = usuarios_repository.obtener_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def crear_usuario(perfil_data: dict):
    try:
        auth_result = registrar_usuario(
            email=perfil_data.pop("email"),
            password=perfil_data.pop("password"),
            perfil_data=perfil_data
        )
        return auth_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")

def actualizar_usuario(user_id: str, perfil_data: dict):
    actualizado = usuarios_repository.actualizar_usuario(user_id, perfil_data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Perfil actualizado correctamente", "usuario": actualizado}

def eliminar_usuario(user_id: str):
    eliminado = usuarios_repository.eliminar_usuario(user_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}
