from src.db.supabase_client import supabase
from datetime import datetime
import json

def _default_serializer(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Tipo no serializable: {type(o)}")

def _serialize_for_supabase(obj):
    return json.loads(json.dumps(obj, default=_default_serializer))

def crear_movimiento(data: dict):
    payload = _serialize_for_supabase(data)
    response = supabase.table("movimientos").insert(payload).execute()
    return response.data

def listar_movimientos():
    response = supabase.table("movimientos").select("*").order("created_at", desc=True).execute()
    return response.data
