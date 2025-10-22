from src.db.supabase_client import supabase

def obtener_usuarios():
    """Obtiene todos los perfiles de usuario."""
    return supabase.table("perfiles").select("*").order("creado_en", desc=True).execute().data

def obtener_usuario_por_id(user_id: str):
    """Obtiene un perfil por su ID."""
    return supabase.table("perfiles").select("*").eq("id", user_id).single().execute().data

def crear_usuario(perfil_data: dict):
    """Crea un nuevo perfil (normalmente después del registro en Supabase Auth)."""
    return supabase.table("perfiles").insert(perfil_data).execute().data

def actualizar_usuario(user_id: str, perfil_data: dict):
    """Actualiza datos del perfil."""
    return supabase.table("perfiles").update(perfil_data).eq("id", user_id).execute().data

def eliminar_usuario(user_id: str):
    """Elimina un perfil."""
    return supabase.table("perfiles").delete().eq("id", user_id).execute().data
