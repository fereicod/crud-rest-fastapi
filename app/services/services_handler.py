from app.services.base import BaseServiceHandler
from app.providers.admin_provider import AdminProvider
from app.providers.product_provider import ProductProvider
from app.services.admin_services import AdminService
from app.services.product_services import ProductService


class AdminServiceHandler(BaseServiceHandler):

    def _setup_repositories(self) -> None:
        self.admin_repo = AdminProvider(self.session)
    
    def _setup_services(self) -> None:
        self.admin_service = AdminService(self.admin_repo)
    
    def get_services(self) -> AdminService:
        return self.admin_service

class ProductServiceHandler(BaseServiceHandler):

    def _setup_repositories(self) -> None:
        self.product_repo = ProductProvider(self.session)
    
    def _setup_services(self) -> None:
        self.product_service = ProductService(self.product_repo)
    
    def get_services(self) -> ProductService:
        return self.product_service