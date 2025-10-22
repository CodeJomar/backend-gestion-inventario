from fastapi import Depends, HTTPException, Header, status
from src.db.supabase_client import supabase
from src.auth.roles import ADMIN

async def get_current_user(authorization: str = Header(...)):
    """Valida el token JWT del usuario logueado."""
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        perfil = supabase.table("perfiles").select("*").eq("id", user.user.id).single().execute()
        if not perfil.data:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")

        return perfil.data
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error de autenticación: {e}")

async def require_admin(current_user=Depends(get_current_user)):
    """Permite acceso solo a administradores."""
    if current_user["rol"] != ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los administradores pueden realizar esta acción.")
    return current_user
