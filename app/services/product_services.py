from typing import Optional
from app.providers.product_provider import ProductProvider
from app.database.models import Product
from app.schemas.api_product import ProductCreate, ProductUpdate
from fastapi import HTTPException


class ProductService:
    def __init__(self, product_repo: ProductProvider):
        self.product_repo = product_repo 

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        product = self.product_repo.get_by_sku(sku)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    def get_all_products(self) -> list[Product]:
        products = self.product_repo.get_all()
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products

    def create_product(self, product: ProductCreate) -> Product:
        existing = self.product_repo.get_by_sku(product.sku)
        if existing:
            raise HTTPException(status_code=400, detail="Product already exists")
        new_product = Product(**product.model_dump())
        return self.product_repo.create(new_product)
    
    def update_product(self, sku: str, data: ProductUpdate) -> Product:
        product = self.product_repo.get_by_sku(sku)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if getattr(product, key) != value:
                setattr(product, key, value)
        return self.product_repo.update(product)
    
    def delete_product(self, sku: str):
        product = self.product_repo.get_by_sku(sku)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        self.product_repo.delete(product)