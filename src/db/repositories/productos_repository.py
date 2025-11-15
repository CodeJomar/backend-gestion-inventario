from src.db.supabase_client import supabase
from decimal import Decimal


#def listar_productos():
#    try:
#        response = supabase.table("productos").select("*").eq("estado", True).order("created_at", desc=True).execute()
#        return response.data
#    except Exception as e:
#        print(f"Error al listar productos: {e}")
#        return []

def listar_productos():
    try:
        activos = (
            supabase.table("productos").select("*").eq("estado", True).order("created_at", desc=True).execute().data
        )

        inactivos = (
            supabase.table("productos").select("*").eq("estado", False).order("created_at", desc=True).execute().data
        )

        return activos + inactivos
        # Los productos deben tener un estado (no nulo) para que se muestren correctamente

    except Exception as e:
        print(f"Error al listar productos: {e}")
        return []


def obtener_producto(id: str):
    try:
        result = supabase.table("productos").select("*").eq("id", id).execute()
        product = result.data[0] if result.data else None
        if product:
                stock = product.get("stock", 0)
                if isinstance(stock, Decimal):
                    product["stock"] = int(stock)
                elif stock is None:
                    product["stock"] = 0
                elif isinstance(stock, str):
                    try:
                        product["stock"] = int(float(stock))
                    except:
                        product["stock"] = 0
        return product
    except Exception as e:
        print(f"Error al obtener producto {id}: {e}")
        return None

def crear_producto(data: dict):
    return supabase.table("productos").insert(data).execute().data

def actualizar_producto(id: str, data: dict):
    return supabase.table("productos").update(data).eq("id", id).execute().data

def desactivar_producto(id: str):
    return supabase.table("productos").update({"estado": False}).eq("id", id).execute().data

def reactivar_producto(id: str):
    return supabase.table("productos").update({"estado": True}).eq("id", id).execute().data

def listar_productos_activos():
    return (supabase.table("productos").select("*").eq("estado", True).order("created_at", desc=True).execute().data)

def listar_productos_inactivos():
    return (supabase.table("productos").select("*").eq("estado", False).order("created_at", desc=True).execute().data)