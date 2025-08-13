from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

# ToDo: Move to /database/handler
db_users={
    "fer": {
        "username":"fer",
        "password":"ferpass#hash"
    }
}
def get_user(username: str) -> Optional[dict]:
    if username in db_users:
        return db_users[username]
    return None
def authenticate_user(password: str, passwod_plain: str) -> bool:
    password_clean = password.split("#")[0]
    return True if password_clean == passwod_plain else False

# ToDo: Move to /utils/auth
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

# ToDo: Move to /schemas/
from pydantic import BaseModel
class Admin(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(admin: Admin):
    user_data = get_user(admin.username)
    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail="Not found user"
        )
    if not authenticate_user(user_data["password"], admin.password):
        raise HTTPException(
            status_code=401,
            detail="Not authorization"
        )
    access_token = create_access_token({"sub": user_data["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/")
def list_admins():
    return list(db_users.keys())