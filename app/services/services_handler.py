from sqlmodel import Session
from fastapi import Depends
from app.database.manager import get_session
from app.services.base import BaseServiceHandler


class AdminServiceHandler(BaseServiceHandler):    
    def get_services(self):
        return self.admin_service


def get_admin_services(session: Session = Depends(get_session)):
    handler = AdminServiceHandler(session)
    return handler.get_services()
