from sqlmodel import Session, select
from typing import Optional
from app.database.models import Admin

class AdminRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[Admin]:
        statement = select(Admin).where(Admin.username == username)
        return self.session.exec(statement).first()
