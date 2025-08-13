from datetime import datetime, timedelta, timezone 
from jwt import encode
from app.core.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES

def expirate_token(expiration_time: str):
    return datetime.now(timezone.utc) + timedelta(minutes=int(expiration_time))

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": expirate_token(EXPIRE_MINUTES)})
    return encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)