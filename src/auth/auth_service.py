from src.db.supabase_client import supabase
from src.auth.roles import EMPLEADO
from fastapi import HTTPException

def registrar_usuario(email: str, password: str, perfil_data: dict):
    """
    Crea el usuario en Supabase Auth y su perfil asociado.
    """
    try:
        # Crear en Supabase Auth
        response = supabase.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True  # activa inmediatamente
        })

        user_id = response.user.id

        # Crear perfil
        perfil_data["id"] = user_id
        perfil_data["rol"] = perfil_data.get("rol", EMPLEADO)

        supabase.table("perfiles").insert(perfil_data).execute()

        return {"mensaje": "Usuario creado correctamente", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")
