from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    brand: str

class ProductCreate(ProductBase):
    sku: str

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    sku: str