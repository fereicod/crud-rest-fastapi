from typing import Optional, Any
from app.providers.admin_provider import AdminProvider
from app.database.models import Admin
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, admin_repo: AdminProvider):
        self.admin_repo = admin_repo

    def get_admin_by_username(self, username: str) -> Optional[Admin]:
        admin = self.admin_repo.get_by_username(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    
    def get_all_admins(self) -> list[Admin]:
        admins = self.admin_repo.get_all()
        if not admins:
            raise HTTPException(status_code=404, detail="No admins found")
        return admins

    def create_admin(self, username: str, password: str, email: Optional[str] = None) -> Admin:
        existing = self.admin_repo.get_by_username(username)
        if existing:
            raise HTTPException(status_code=400, detail="Admin already exists")
        hashed = pwd_ctx.hash(password)
        admin = Admin(username=username, password=hashed, email=email)
        return self.admin_repo.create(admin)

    def update_admin(self, username: str, data: Any) -> Admin:
        admin = self.admin_repo.get_by_username(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        if data.username:
            admin.username = data.username
        if data.email:
            admin.email = data.email
        return self.admin_repo.update(admin)
    
    def delete_admin(self, username: str):
        admin = self.admin_repo.get_by_username(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        self.admin_repo.delete(admin)
    
    def authenticate_credentials(self, username: str, password: str) -> Admin:
        admin = self.admin_repo.get_by_username(username)
        if not admin:
            raise HTTPException(status_code=401, detail="Admin not found")
        if not pwd_ctx.verify(password, admin.password):
            raise HTTPException(status_code=401, detail="Not authorization")
        return admin