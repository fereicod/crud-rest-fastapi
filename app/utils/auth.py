from datetime import datetime, timedelta, timezone 
from jwt import encode
from app.core.config import settings

SECRET_KEY: str =  settings.JWT_SECRET
ALGORITHM: str =  settings.JWT_ALGORITHM
EXPIRE_MINUTES: str =  settings.JWT_EXPIRE_MINUTES

def expirate_token(expiration_time: str) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=int(expiration_time))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expirate_token(EXPIRE_MINUTES)})
    return encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
