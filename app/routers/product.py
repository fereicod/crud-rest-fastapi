from collections import defaultdict
from typing import Union
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from app.schemas.api_product import Product, ProductCreate, ProductUpdate
from app.middleware.auth_middleware import verify_token, verify_token_optional
from app.services.services import get_product_services
from app.utils.notifier import notify_admins

router = APIRouter()


product_query_count: dict[str, int] = defaultdict(int)

@router.get("/statistics")
def get_product_statistics(_=Depends(verify_token)):
    return dict(product_query_count)

@router.get("/all", response_model=list[Product])
def list_products(product_services=Depends(get_product_services)):
    return product_services.get_all_products()

@router.get("/{sku}", response_model=Product)
def get_product(sku: str, token=Depends(verify_token_optional), product_services=Depends(get_product_services)):
    if not token:
        product_query_count[sku] += 1
    return product_services.get_product_by_sku(sku)
    

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, _=Depends(verify_token), product_services=Depends(get_product_services)):
    return product_services.create_product(product)

@router.put("/{sku}", response_model=Product)
def update_product(sku: str, product: ProductUpdate, background_tasks: BackgroundTasks, user=Depends(verify_token), product_services=Depends(get_product_services)):
    updated_product = product_services.update_product(sku, product)
    notify_admins(sku, user, background_tasks)
    return updated_product

@router.delete("/{sku}")
def delete_product(sku: str, _=Depends(verify_token), product_services=Depends(get_product_services)):
    product_services.delete_product(sku)
    return {"detail": "Product deleted"}
    