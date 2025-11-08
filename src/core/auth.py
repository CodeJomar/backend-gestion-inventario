from typing import Optional, Sequence
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from src.db.supabase_client import supabase


@dataclass
class CurrentUser:
    id: str
    email: str
    role_id: Optional[str]
    role_name: Optional[str]
    permissions: set[str]


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    token = _extract_bearer_token(authorization)

    # 1) Validate JWT and get auth user
    try:
        auth_res = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = getattr(auth_res, "user", None)
    if not user or not getattr(user, "id", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = user.id
    email = getattr(user, "email", "") or ""

    # 2) Load profile
    perfil_res = supabase.table("perfiles").select("*").eq("id", user_id).single().execute()
    perfil = (perfil_res.data or {}) if hasattr(perfil_res, "data") else {}
    
    is_blocked = perfil.get("eliminado_por") != None
    
    if is_blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User has been blocked")

    role_id = perfil.get("role_id")
    role_name: Optional[str] = None

    # 3) Resolve role name
    if role_id:
        role_res = supabase.table("roles").select("name").eq("id", role_id).single().execute()
        role_name = (role_res.data or {}).get("name") if hasattr(role_res, "data") else None

    # 4) Resolve permissions
    permissions: set[str] = set()
    if role_id:
        rp_res = supabase.table("role_permissions").select("permission_id").eq("role_id", role_id).execute()
        rp = rp_res.data or []
        perm_ids = [row["permission_id"] for row in rp if row.get("permission_id")]
        if perm_ids:
            perms_res = supabase.table("permissions").select("id,name").in_("id", perm_ids).execute()
            for p in (perms_res.data or []):
                if p.get("name"):
                    permissions.add(p["name"])

    return CurrentUser(
        id=user_id,
        email=email,
        role_id=role_id,
        role_name=role_name,
        permissions=permissions,
    )


def require_roles(*allowed_roles: str):
    def _dep(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current.role_name or current.role_name not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current
    return _dep


def require_permissions(*required: str):
    required_set = set(required)
    def _dep(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not required_set.issubset(current.permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current
    return _dep


def require_any_permission(*candidates: str):
    candidates_set = set(candidates)
    def _dep(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not (current.permissions & candidates_set):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current
    return _dep