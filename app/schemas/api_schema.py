from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class Admin(BaseModel):
    id: int
    username: str
    email: str

class Product(BaseModel):
    sku: str
    name: str
    price: float
    brand: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"