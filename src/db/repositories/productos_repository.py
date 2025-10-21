from src.db.supabase_client import supabase

def listar_productos():
    try:
        response = supabase.table("productos").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error al listar productos: {e}")
        return []

def obtener_producto(id: str):
    try:
        result = supabase.table("productos").select("*").eq("id", id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error al obtener producto {id}: {e}")
        return None

def crear_producto(data: dict):
    return supabase.table("productos").insert(data).execute().data

def actualizar_producto(id: str, data: dict):
    return supabase.table("productos").update(data).eq("id", id).execute().data

def eliminar_producto(id: str):
    return supabase.table("productos").delete().eq("id", id).execute().data