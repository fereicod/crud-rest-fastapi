import pytest
from fastapi import HTTPException, BackgroundTasks
from unittest.mock import patch
from app.routers.product import (
    list_products, get_product, create_product, 
    update_product, delete_product,
    products
)
from app.schemas.api_product import ProductCreate, ProductUpdate

@pytest.fixture
def test_product():
    return {
        "name": "Test Product",
        "price": 1.0,
        "brand": "Brand",
        "sku": "99999-Z"
    }

def test_list_products():
    result = list_products()
    assert isinstance(result, list)
    assert "sku" in result[0]

@patch('app.routers.product.verify_token_optional', return_value=None)
def test_get_product_success(mock_verify):
    sku = products[0]["sku"]
    result = get_product(sku)
    assert result["sku"] == sku

@patch('app.routers.product.verify_token_optional', return_value=None)
def test_get_product_not_found(mock_verify):
    with pytest.raises(HTTPException):
        get_product("notfound")

@patch('app.routers.product.verify_token', return_value=True)
def test_create_product_success(mock_verify, test_product):
    prod = ProductCreate(**test_product)
    result = create_product(prod)
    assert result["sku"] == test_product["sku"]
    products.pop()

@patch('app.routers.product.verify_token', return_value=True)
def test_create_product_duplicate(mock_verify):
    sku = products[0]["sku"]
    prod = ProductCreate(
        name="Test",
        price=1.0,
        brand="Brand",
        sku=sku
    )
    with pytest.raises(HTTPException):
        create_product(prod)

@patch('app.routers.product.verify_token')
@patch('app.routers.product.notify_admins')
def test_update_product_success(mock_notify, mock_verify):
    mock_verify.return_value = {"sub": "test_user"}
    prod = ProductUpdate(name="Updated", price=2.0, brand="Brand")
    sku = products[0]["sku"]
    
    result = update_product(sku, prod, BackgroundTasks(), mock_verify.return_value)
    assert result["name"] == "Updated"
    mock_notify.assert_called_once()

@patch('app.routers.product.verify_token')
def test_update_product_not_found(mock_verify):
    mock_verify.return_value = {"sub": "test_user"}
    prod = ProductUpdate(name="Updated", price=2.0, brand="Brand")
    
    with pytest.raises(HTTPException):
        update_product("notfound", prod, BackgroundTasks(), mock_verify.return_value)

@patch('app.routers.product.verify_token', return_value=True)
def test_delete_product_success(mock_verify):
    products.append({
        "id": 999,
        "sku": "99999-Z",
        "name": "Test",
        "price": 1.0,
        "brand": "Brand"
    })
    
    result = delete_product("99999-Z")
    assert result["detail"] == "Product deleted"

@patch('app.routers.product.verify_token', return_value=True)
def test_delete_product_not_found(mock_verify):
    with pytest.raises(HTTPException):
        delete_product("notfound")