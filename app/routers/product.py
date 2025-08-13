from collections import defaultdict
from typing import Union
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from app.schemas.api_product import Product, ProductCreate, ProductUpdate
from app.middleware.auth_middleware import verify_token, verify_token_optional
from app.utils.notifier import notify_admins

router = APIRouter()

products: list[dict[str, Union[int, float, str]]] = [
    {"id":1, "sku": "10001-A", "name": "Wireless Mouse", "price": 19.99, "brand": "LogiTech"},
    {"id":2, "sku": "10002-B", "name": "Mechanical Keyboard", "price": 49.99, "brand": "KeyMaster"},
    {"id":3, "sku": "10003-C", "name": "27-inch Monitor", "price": 179.99, "brand": "ViewPlus"},
    {"id":4, "sku": "10004-D", "name": "USB-C Hub", "price": 25.50, "brand": "Hubify"},
    {"id":5, "sku": "10005-E", "name": "External SSD 1TB", "price": 129.99, "brand": "FastStorage"},
    {"id":6, "sku": "10006-F", "name": "Noise Cancelling Headphones", "price": 89.99, "brand": "SoundMax"},
    {"id":7, "sku": "10007-G", "name": "Webcam HD", "price": 39.99, "brand": "CamTech"},
    {"id":8, "sku": "10008-H", "name": "Smartphone Stand", "price": 12.99, "brand": "PhoneMate"},
    {"id":9, "sku": "10009-I", "name": "Portable Charger 10000mAh", "price": 29.99, "brand": "PowerGo"},
    {"id":10, "sku": "10010-J", "name": "Bluetooth Speaker", "price": 59.99, "brand": "SoundWave"}
]

product_query_count: dict[str, int] = defaultdict(int)

@router.get("/statistics")
def get_product_statistics(_=Depends(verify_token)):
    return dict(product_query_count)

@router.get("/all", response_model=list[Product])
def list_products():
    return products

@router.get("/{sku}", response_model=Product)
def get_product(sku: str, token=Depends(verify_token_optional)):
    for p in products:
        if p["sku"] == sku:
            if not token:
                product_query_count[sku] += 1
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, _=Depends(verify_token)):
    for p in products:
        if p["sku"] == product.sku:
            raise HTTPException(status_code=400, detail="Product already exists")

    new_id = max((int(p["id"]) for p in products), default=0) + 1
    new_product: dict[str, Union[int, float, str]] = product.dict()
    new_product["id"] = new_id
    products.append(new_product)
    return new_product

@router.put("/{sku}", response_model=Product)
def update_product(sku: str, product: ProductUpdate, background_tasks: BackgroundTasks, user=Depends(verify_token)):
    user = user["sub"]
    for idx, p in enumerate(products):
        if p["sku"] == sku:
            products[idx].update(product.dict())
            notify_admins(products[idx], user, background_tasks)
            return products[idx]
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{sku}")
def delete_product(sku: str, _=Depends(verify_token)):
    for idx, p in enumerate(products):
        if p["sku"] == sku:
            products.pop(idx)
            return {"detail": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
    