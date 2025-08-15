from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, InvalidTokenError
from app.services.services import get_admin_services
from app.services.admin_services import AdminService
from app.core.config import settings

SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.JWT_ALGORITHM

security = HTTPBearer(auto_error=False)

def _decode_token(token: str, admin_services: Optional[AdminService]) -> dict:
    try:
        payload: dict = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if admin_services and isinstance(user, str):
            admin_services.get_admin_by_username(username=user)
            return payload
        raise HTTPException(status_code=401, detail="Invalid token by user")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), admin_services=Depends(get_admin_services)) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token required")
    return _decode_token(credentials.credentials, admin_services)

# Token opcional
def verify_token_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), 
) -> Optional[dict]:
    if credentials is None:
        return None
    try:
        return _decode_token(credentials.credentials, None)
    except HTTPException:
        return None


