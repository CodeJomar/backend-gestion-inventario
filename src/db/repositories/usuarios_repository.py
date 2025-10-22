from src.db.supabase_client import supabase

def crear_usuario(data: dict):
    email = data["email"]
    password = data["password"]

    # Crear usuario en Supabase Auth
    response_auth = supabase.auth.admin.create_user(
        {
            "email": email,
            "password": password,
            "email_confirm": True
        }
    )

    if not response_auth.user:
        raise Exception("No se pudo crear el usuario en Supabase Auth")

    user_id = response_auth.user.id

    # Crear perfil asociado
    perfil_data = {
        "id": user_id,
        "email": email,
        "nombres": data["nombres"],
        "apellidos": data["apellidos"],
        "usuario": data["usuario"],
        "celular": data["celular"],
        "dni": data["dni"],
        "rol": data["rol"],
        "creado_por": data.get("creado_por")
    }

    supabase.table("perfiles").insert(perfil_data).execute()

    return {"mensaje": "Usuario creado correctamente", "user_id": user_id}


def listar_usuarios():
    response = supabase.table("perfiles").select("*").order("created_at", desc=False).execute()
    return response.data


def obtener_usuario_por_id(usuario_id: str):
    response = supabase.table("perfiles").select("*").eq("id", usuario_id).execute()
    return response.data[0] if response.data else None


def actualizar_usuario(usuario_id: str, data: dict):
    response = supabase.table("perfiles").update(data).eq("id", usuario_id).execute()
    return response.data


def eliminar_usuario(usuario_id: str):
    """
    Elimina el perfil y desactiva el usuario en Supabase Auth.
    """
    # Desactivar usuario en auth
    supabase.auth.admin.update_user_by_id(usuario_id, {"banned_until": "2999-12-31T23:59:59Z"})

    # Borrar perfil
    supabase.table("perfiles").delete().eq("id", usuario_id).execute()

    return {"mensaje": "Usuario eliminado correctamente"}
