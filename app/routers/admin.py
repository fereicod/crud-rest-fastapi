from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.utils.auth import create_access_token
from app.schemas.api_admin import Token, AdminLogin, Admin, AdminCreate, AdminUpdate
from app.middleware.auth_middleware import verify_token
from app.services.services import get_admin_services

router = APIRouter()

@router.post("/login", response_model=Token)
def login(admin: AdminLogin, admin_services=Depends(get_admin_services)):
    admin = admin_services.authenticate_credentials(admin.username, admin.password)
    access_token = create_access_token({"sub": admin.username})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/all", response_model=list[Admin])
def list_admins(_=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.get_all_admins()

@router.get("/{username}", response_model=Admin)
def get_admin(username: str, _=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.get_admin_by_username_active(username)

@router.post("/", response_model=Admin)
def create_admin(admin: AdminCreate, _=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.create_admin(admin)

@router.put("/{username}", response_model=Admin)
def update_admin(username: str, admin: AdminUpdate, _=Depends(verify_token), admin_services=Depends(get_admin_services)):
    return admin_services.update_admin(username, admin)

@router.delete("/{username}")
def delete_admin(username: str, _=Depends(verify_token), admin_services=Depends(get_admin_services)):
    admin_services.delete_admin(username)
    return {"detail": "Admin deleted"}