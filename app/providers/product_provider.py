from sqlmodel import Session, select
from typing import Optional
from app.database.models import Product

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        statement = select(Product).where(Product.sku == sku)
        return self.session.exec(statement).first()

