from typing import Optional, Any
from app.providers.admin_provider import AdminProvider
from app.database.models import Admin
from app.schemas.api_admin import AdminCreate, AdminUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, admin_repo: AdminProvider):
        self.admin_repo = admin_repo

    def get_admin_by_username_active(self, username: str) -> Optional[Admin]:
        admin = self.admin_repo.get_by_username_and_active(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    
    def get_all_admins(self) -> list[Admin]:
        admins = self.admin_repo.get_all()
        if not admins:
            raise HTTPException(status_code=404, detail="No admins found")
        return admins

    def create_admin(self, admin: AdminCreate) -> Admin:
        existing = self.admin_repo.get_by_username_and_active(admin.username)
        if existing:
            raise HTTPException(status_code=400, detail="Admin already exists")
        hashed = pwd_ctx.hash(admin.password)
        new_admin = Admin(**admin.model_dump(exclude={"password"}), password=hashed)
        return self.admin_repo.create(new_admin)

    def update_admin(self, username: str, data: AdminUpdate) -> Admin:
        admin = self.admin_repo.get_by_username_and_active(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if getattr(admin, key) != value:
                setattr(admin, key, value)
        return self.admin_repo.update(admin)
    
    def delete_admin(self, username: str):
        admin = self.admin_repo.get_by_username_and_active(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        self.admin_repo.delete(admin)
    
    def authenticate_credentials(self, username: str, password: str) -> Admin:
        admin = self.admin_repo.get_by_username_and_active(username)
        if not admin:
            raise HTTPException(status_code=401, detail="Admin not authorized")
        if not pwd_ctx.verify(password, admin.password):
            raise HTTPException(status_code=401, detail="Not authorization")
        return admin