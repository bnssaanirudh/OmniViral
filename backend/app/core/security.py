"""
JWT Security, Password Hashing, and RBAC.
"""
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.core.config import settings


# ── Password Hashing ──────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ── Roles ─────────────────────────────────────────────────────────────────────
class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    AGENT = "agent"


ROLE_PERMISSIONS: dict[Role, list[str]] = {
    Role.ADMIN: ["*"],
    Role.EDITOR: ["ingest", "predict", "forecast", "optimize", "publish"],
    Role.VIEWER: ["predict", "forecast", "metrics", "dashboard"],
    Role.AGENT: ["predict", "forecast", "optimize"],
}


def check_permission(role: Role, action: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, [])
    return "*" in perms or action in perms


# ── JWT Tokens ────────────────────────────────────────────────────────────────
def create_access_token(
    subject: str,
    role: Role = Role.VIEWER,
    expires_delta: Optional[timedelta] = None,
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": subject,
        "role": role.value,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str, role: Role = Role.VIEWER) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "role": role.value,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e


def verify_access_token(token: str) -> dict:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise ValueError("Not an access token")
    return payload
