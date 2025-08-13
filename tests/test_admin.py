import pytest
from fastapi import HTTPException
from unittest.mock import patch
from app.routers.admin import (
    get_user, authenticate_user, login, 
    create_admin, update_admin, delete_admin, 
    db_users
)
from app.schemas.api_admin import AdminLogin, AdminCreate, AdminUpdate

@pytest.mark.parametrize("username,exists", [
    ("fer", True),
    ("notfound", False)
])
def test_get_user(username, exists):
    result = get_user(username)
    if exists:
        assert result["username"] == username
    else:
        assert result is None

@pytest.mark.parametrize("stored_pass,input_pass,valid", [
    ("pass#hash", "pass", True),
    ("pass#hash", "wrong", False)
])
def test_authenticate_user(stored_pass, input_pass, valid):
    assert authenticate_user(stored_pass, input_pass) is valid

@patch('app.routers.admin.create_access_token', return_value="token")
def test_login_success(mock_token):
    admin = AdminLogin(username="fer", password="ferpass")
    result = login(admin)
    assert result.access_token == "token"

@pytest.mark.parametrize("test_data", [
    {"username": "notfound", "password": "pass"},
    {"username": "fer", "password": "wrong"}
])
def test_login_fails(test_data):
    admin = AdminLogin(**test_data)
    with pytest.raises(HTTPException):
        login(admin)

@patch('app.routers.admin.verify_token', return_value=True)
def test_create_admin_success(mock_verify):
    admin = AdminCreate(username="newuser", email="new@ex.com", password="pw")
    result = create_admin(admin)
    assert result["username"] == "newuser"
    db_users.pop("newuser")

@patch('app.routers.admin.verify_token', return_value=True)
def test_create_admin_exists(mock_verify):
    admin = AdminCreate(username="fer", email="fer@ex.com", password="pw")
    with pytest.raises(HTTPException):
        create_admin(admin)

@patch('app.routers.admin.verify_token', return_value=True)
def test_update_admin_success(mock_verify):
    admin = AdminUpdate(username="fer", email="fer@ex.com")
    result = update_admin("fer", admin)
    assert result["username"] == "fer"

@patch('app.routers.admin.verify_token', return_value=True)
def test_update_admin_not_found(mock_verify):
    admin = AdminUpdate(username="notfound", email="not@ex.com")
    with pytest.raises(HTTPException):
        update_admin("notfound", admin)

@patch('app.routers.admin.verify_token', return_value=True)
def test_delete_admin_success(mock_verify):
    db_users["temp"] = {
        "id": 99, 
        "username": "temp", 
        "email": "temp@gmail.com", 
        "password": "pass"
    }
    
    result = delete_admin("temp")
    assert result["detail"] == "Admin deleted"

@patch('app.routers.admin.verify_token', return_value=True)
def test_delete_admin_not_found(mock_verify):
    with pytest.raises(HTTPException):
        delete_admin("notfound")