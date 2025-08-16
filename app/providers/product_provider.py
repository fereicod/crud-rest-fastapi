from sqlmodel import Session, select
from typing import Optional
from app.database.models import Product

class ProductProvider:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        statement = select(Product).where(Product.sku == sku)
        return self.session.exec(statement).first()

    def get_all(self) -> list[Product]:
        statement = select(Product)
        return list(self.session.exec(statement))

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
    
    def update(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product):
        self.session.delete(product)
        self.session.commit()