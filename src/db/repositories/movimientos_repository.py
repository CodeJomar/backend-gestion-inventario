from src.db.supabase_client import supabase

def listar_movimientos():
    response = supabase.table("movimientos").select("*").order("created_at", desc=True).execute()
    return response.data

def crear_movimiento(data: dict):
    response = supabase.table("movimientos").insert(data).execute()
    return response.data
