import datetime
from typing import Optional
from schemas.usuario import UsuarioCreate
from src.db.supabase_client import supabase

def crear_usuario(usuario: UsuarioCreate, creado_por: Optional[str] = None):
    """
    Crea un usuario en Supabase Auth y su perfil asociado.
    Si falla la creación del perfil, elimina automáticamente el usuario de Auth.

    Args:
        usuario (UsuarioCreate): Datos del usuario.
        creado_por (str, optional): ID del usuario que crea este usuario.

    Returns:
        dict: Mensaje de éxito y user_id

    Raises:
        Exception: Si falla la creación del usuario o perfil
    """
    email = usuario.email
    password = usuario.password

    # 1. Crear usuario en Supabase Auth
    try:
        response_auth = supabase.auth.sign_up({"email": email, "password": password})
        if not response_auth.user:
            raise Exception("No se pudo crear el usuario en Supabase Auth")
        user_id = response_auth.user.id
    except Exception as e:
        raise Exception(f"Error al crear usuario en Supabase Auth: {str(e)}")

    # 2. Obtener role_id
    try:
        role_id = None
        if usuario.rol:
            role_resp = supabase.table("roles").select("id").eq("name", usuario.rol).single().execute()
            if not role_resp.data:
                raise Exception(f"Rol '{usuario.rol}' no encontrado")
            role_id = role_resp.data["id"]

        # Asignar rol por defecto si no se pasó uno
        if not role_id:
            default_role_resp = supabase.table("roles").select("id").eq("name", "Usuario").single().execute()
            if not default_role_resp.data:
                raise Exception("No se pudo asignar el rol por defecto")
            role_id = default_role_resp.data["id"]
    except Exception as e:
        # Eliminar usuario creado de Auth si falla la asignación de rol
        try:
            supabase.auth.admin.delete_user(user_id)
        except Exception:
            pass
        raise Exception(f"Error al obtener role_id: {str(e)}")

    # 3. Crear perfil en la tabla perfiles
    perfil_data = {
        "id": user_id,
        "email": email,
        "nombres": usuario.nombres,
        "apellidos": usuario.apellidos,
        "usuario": usuario.usuario,
        "celular": usuario.celular,
        "dni": usuario.dni,
        "creado_por": creado_por,
        "role_id": role_id
    }

    try:
        perfil_resp = supabase.table("perfiles").insert(perfil_data).execute()
        if not perfil_resp.data:
            raise Exception("No se pudo crear el perfil del usuario")
    except Exception as e:
        # Limpieza: eliminar usuario de Auth si falla la creación del perfil
        try:
            supabase.auth.admin.delete_user(user_id)
        except Exception as delete_error:
            # No romper el flujo principal, solo loggear
            print(f"No se pudo eliminar usuario huérfano: {delete_error}")
        raise Exception(f"Error al crear el perfil del usuario: {str(e)}")

    return {"mensaje": "Usuario creado correctamente", "user_id": user_id}


def listar_usuarios():
    response = supabase.table("perfiles").select("*").order("created_at", desc=False).execute()
    
    roles_response = supabase.table("roles").select("id, name").execute()
    roles = roles_response.data or []
    role_map = {role["id"]: role["name"] for role in roles}
    data = [
        {
            **user, 
            'active': bool(user.get('eliminado_por', None) == None),
            "rol": role_map.get(user.get("role_id"))
        }
        for user in response.data
    ]
    return data


def obtener_usuario_por_id(usuario_id: str):
    response = supabase.table("perfiles").select("*").eq("id", usuario_id).execute()
    return response.data[0] if response.data else None


def actualizar_usuario(usuario_id: str, data: dict, modifier_id: str):
    # Manejar estado activo / baneado
    is_active = data.pop("active", True)
    if not is_active:
        supabase.auth.admin.update_user_by_id(
            usuario_id, {"banned_until": "2999-12-31T23:59:59Z"}
        )
        data['eliminado_por'] = modifier_id
        data['deleted_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    else:
        supabase.auth.admin.update_user_by_id(
            usuario_id, {"banned_until": None}
        )
        data['eliminado_por'] = None
        data['deleted_at'] = None

    # Convertir 'rol' a 'role_id' si aplica
    if "rol" in data:
        role_name = data["rol"]
        role_res = supabase.table("roles").select("id").eq("name", role_name).single().execute()
        if not role_res.data:
            raise Exception(f"Rol '{role_name}' no encontrado en la base de datos")
        data["role_id"] = role_res.data["id"]
        del data["rol"]

    # Actualizar tabla 'perfiles' solo si hay datos
    if data:
        update_res = supabase.table("perfiles").update(data).eq("id", usuario_id).execute()
        if update_res.data is None or len(update_res.data) == 0:
            raise Exception(f"No se pudo actualizar el perfil {usuario_id}")

    # Devolver siempre el perfil actualizado
    perfil_res = supabase.table("perfiles").select("*").eq("id", usuario_id).single().execute()
    return perfil_res.data


def eliminar_usuario(usuario_id: str):
    """
    Elimina el perfil y desactiva el usuario en Supabase Auth.
    """
    # Desactivar usuario en auth
    supabase.auth.admin.update_user_by_id(usuario_id, {"banned_until": "2999-12-31T23:59:59Z"})

    # Borrar perfil
    supabase.table("perfiles").delete().eq("id", usuario_id).execute()

    return {"mensaje": "Usuario eliminado correctamente"}