from typing import Optional
from app.repositories.admim_repository import AdminRepository
from app.database.models import Admin
from fastapi import HTTPException


class AdminService:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def get_admin_by_username(self, username: str) -> Optional[Admin]:
        admin = self.admin_repo.get_by_username(username)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin