from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.db.supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
def login(data: LoginRequest):
    """
    Authenticates a user with Supabase Auth and returns a JWT + user info.
    """
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": data.email, "password": data.password}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {e}",
        )

    session = getattr(res, "session", None)
    user = getattr(res, "user", None)
    if not session or not getattr(session, "access_token", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "user": {
            "id": user.id if user else None,
            "email": user.email if user else None,
        },
    }
