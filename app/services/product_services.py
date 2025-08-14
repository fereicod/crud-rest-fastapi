from typing import Optional
from app.repositories.product_repository import ProductRepository
from app.database.models import Product
from fastapi import HTTPException


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo 

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        product = self.product_repo.get_by_sku(sku)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product