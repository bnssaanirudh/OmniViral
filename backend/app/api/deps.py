"""
FastAPI dependency injection: auth, DB, RBAC.
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import Role, verify_access_token

bearer_scheme = HTTPBearer()


# ── Database ──────────────────────────────────────────────────────────────────
DBSession = Annotated[AsyncSession, Depends(get_db)]


# ── Auth ──────────────────────────────────────────────────────────────────────
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> dict:
    """Extract and verify the JWT bearer token."""
    try:
        payload = verify_access_token(credentials.credentials)
        return {
            "sub": payload["sub"],
            "role": Role(payload["role"]),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


CurrentUser = Annotated[dict, Depends(get_current_user)]


def require_role(*roles: Role):
    """Dependency factory: requires the current user to have one of the given roles."""
    async def _check(user: CurrentUser):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user['role']}' is not authorized for this action.",
            )
        return user
    return _check


AdminOnly = Depends(require_role(Role.ADMIN))
EditorOrAdmin = Depends(require_role(Role.EDITOR, Role.ADMIN))
