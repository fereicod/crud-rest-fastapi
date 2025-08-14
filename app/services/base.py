from sqlmodel import Session
from app.repositories.admim_repository import AdminRepository
from app.services.admin_services import AdminService

class BaseServiceHandler:    
    def __init__(self, session: Session):
        self.session = session
        self._setup_repositories()
        self._setup_services()
    
    def _setup_repositories(self):
        self.admin_repo = AdminRepository(self.session)
    
    def _setup_services(self):
        self.admin_service = AdminService(self.admin_repo)