"""Authentication router: register, login, refresh, me."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import DBSession, CurrentUser
from backend.app.core.security import (
    Role,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_access_token,
)

router = APIRouter()


# ── Schemas (inline for auth) ─────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.VIEWER


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class UserResponse(BaseModel):
    username: str
    email: str
    role: Role


# ── In-memory user store (replace with DB in production) ─────────────────────
_USERS: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "email": "admin@omniviral.ai",
        "hashed_password": hash_password("admin123"),
        "role": Role.ADMIN,
    }
}


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(request: RegisterRequest):
    """Register a new user."""
    if request.username in _USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{request.username}' already exists.",
        )
    _USERS[request.username] = {
        "username": request.username,
        "email": request.email,
        "hashed_password": hash_password(request.password),
        "role": request.role,
    }
    return UserResponse(
        username=request.username, email=request.email, role=request.role
    )


@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login with username/password, returns JWT tokens."""
    user = _USERS.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(
        access_token=create_access_token(user["username"], user["role"]),
        refresh_token=create_refresh_token(user["username"], user["role"]),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Exchange a refresh token for a new access token."""
    try:
        payload = verify_access_token(refresh_token)
        username = payload["sub"]
        role = Role(payload["role"])
        return TokenResponse(
            access_token=create_access_token(username, role),
            refresh_token=create_refresh_token(username, role),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    """Return the current authenticated user."""
    username = current_user["sub"]
    user = _USERS.get(username, {})
    return UserResponse(
        username=username,
        email=user.get("email", ""),
        role=current_user["role"],
    )
