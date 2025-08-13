from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.utils.auth import create_access_token
from app.schemas.api_schema import Product
from app.middleware.auth_middleware import verify_token

router = APIRouter()

products = [
    {"sku": "10001-A", "name": "Wireless Mouse", "price": 19.99, "brand": "LogiTech"},
    {"sku": "10002-B", "name": "Mechanical Keyboard", "price": 49.99, "brand": "KeyMaster"},
    {"sku": "10003-C", "name": "27-inch Monitor", "price": 179.99, "brand": "ViewPlus"},
    {"sku": "10004-D", "name": "USB-C Hub", "price": 25.50, "brand": "Hubify"},
    {"sku": "10005-E", "name": "External SSD 1TB", "price": 129.99, "brand": "FastStorage"},
    {"sku": "10006-F", "name": "Noise Cancelling Headphones", "price": 89.99, "brand": "SoundMax"},
    {"sku": "10007-G", "name": "Webcam HD", "price": 39.99, "brand": "CamTech"},
    {"sku": "10008-H", "name": "Smartphone Stand", "price": 12.99, "brand": "PhoneMate"},
    {"sku": "10009-I", "name": "Portable Charger 10000mAh", "price": 29.99, "brand": "PowerGo"},
    {"sku": "10010-J", "name": "Bluetooth Speaker", "price": 59.99, "brand": "SoundWave"}
]


@router.get("/", response_model=list[Product])
def list_products():
    return products