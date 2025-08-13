from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, InvalidTokenError
from app.core.config import settings

SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = settings.JWT_ALGORITHM

security = HTTPBearer(auto_error=False)

def _decode_token(token: str) -> dict:
    try:
        payload: dict = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Token required")
    return _decode_token(credentials.credentials)

# Token opcional
def verify_token_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    if credentials is None:
        return None
    try:
        return _decode_token(credentials.credentials)
    except HTTPException:
        return None
