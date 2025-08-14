from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.utils.auth import create_access_token
from app.schemas.api_admin import Token, AdminLogin, Admin, AdminCreate, AdminUpdate
from app.middleware.auth_middleware import verify_token
from app.services.services import get_admin_services

router = APIRouter()

# ToDo: Move to /database/handler
db_users: dict[str, dict] = {
    "fer": {
        "id": 1,
        "username": "fer",
        "email": "mferna.92@gmail.com",
        "password": "ferpass#hash"
    },
    "ana": {
        "id": 2,
        "username": "ana",
        "email": "ana@example.com",
        "password": "ana123#hash"
    },
    "luis": {
        "id": 3,
        "username": "luis",
        "email": "luis@example.com",
        "password": "luis123#hash"
    },
    "maria": {
        "id": 4,
        "username": "maria",
        "email": "maria@example.com",
        "password": "maria123#hash"
    },
    "jose": {
        "id": 5,
        "username": "jose",
        "email": "jose@example.com",
        "password": "jose123#hash"
    },
    "carla": {
        "id": 6,
        "username": "carla",
        "email": "carla@example.com",
        "password": "carla123#hash"
    }
}

def get_user(username: str) -> Optional[dict]:
    if username in db_users:
        return db_users[username]
    return None
def authenticate_user(password: str, passwod_plain: str) -> bool:
    password_clean = password.split("#")[0]
    return True if password_clean == passwod_plain else False

@router.post("/login", response_model=Token)
def login(admin: AdminLogin):
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
    return Token(access_token=access_token, token_type="bearer")

@router.get("/all", response_model=list[Admin])
def list_admins(_=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.get_all_admins()

@router.get("/{username}", response_model=Admin)
def get_admin(username: str, _=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.get_admin_by_username(username)

@router.post("/", response_model=Admin)
def create_admin(admin: AdminCreate, _=Depends(verify_token)):
    if admin.username in db_users:
        raise HTTPException(status_code=400, detail="Admin already exists")
    new_id = max([int(u["id"]) for u in db_users.values()], default=0) + 1
    db_users[admin.username] = {**admin.dict(), "id": new_id}
    return db_users[admin.username]

@router.put("/{username}", response_model=Admin)
def update_admin(username: str, admin: AdminUpdate, _=Depends(verify_token)):
    if username not in db_users:
        raise HTTPException(status_code=404, detail="Admin not found")
    db_users[username].update(admin.dict())
    return db_users[username]

@router.delete("/{username}")
def delete_admin(username: str, _=Depends(verify_token)):
    if username not in db_users:
        raise HTTPException(status_code=404, detail="Admin not found")
    del db_users[username]
    return {"detail": "Admin deleted"}