import pytest
from datetime import datetime
from unittest.mock import patch
from app.utils.auth import expirate_token, create_access_token

@patch('app.utils.auth.EXPIRE_MINUTES', '10')
def test_expirate_token():
    dt = expirate_token("10")
    assert isinstance(dt, datetime)

@patch('app.utils.auth.EXPIRE_MINUTES', '10')
@patch('app.utils.auth.encode')
def test_create_access_token(mock_encode):
    mock_encode.return_value = "token"
    token = create_access_token({"sub": "user"})

    assert token == "token"
    mock_encode.assert_called_once()