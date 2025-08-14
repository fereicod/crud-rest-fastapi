from app.services.base import BaseServiceHandler
from app.providers.admin_provider import AdminProvider
from app.services.admin_services import AdminService

class AdminServiceHandler(BaseServiceHandler):

    def _setup_repositories(self) -> None:
        self.admin_repo = AdminProvider(self.session)
    
    def _setup_services(self) -> None:
        self.admin_service = AdminService(self.admin_repo)
    
    def get_services(self) -> AdminService:
        return self.admin_service
