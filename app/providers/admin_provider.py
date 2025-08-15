from sqlmodel import Session, select
from typing import Optional
from app.database.models import Admin

class AdminProvider:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[Admin]:
        statement = select(Admin).where(Admin.username == username)
        return self.session.exec(statement).first()
    
    def get_all(self) -> list[Admin]:
        statement = select(Admin)
        return list(self.session.exec(statement))

    def create(self, admin: Admin) -> Admin:
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin
    
    def update(self, admin: Admin) -> Admin:
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    def delete(self, admin: Admin):
        self.session.delete(admin)
        self.session.commit()