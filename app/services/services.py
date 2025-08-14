from fastapi import Depends
from sqlmodel import Session
from app.database.manager import get_session
from app.services.services_handler import AdminServiceHandler


def get_admin_services(session: Session = Depends(get_session)):
    handler = AdminServiceHandler(session)
    return handler.get_services()
