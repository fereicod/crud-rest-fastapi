import pytest
from fastapi import HTTPException
from jwt import InvalidTokenError
from unittest.mock import patch, MagicMock
from app.middleware.auth_middleware import _decode_token, verify_token, verify_token_optional
from app.core.config import settings

class TestDecodeToken:
    @patch('app.middleware.auth_middleware.decode')
    def test_decode_token_valid(self, mock_decode):
        expected_payload = {"sub": "user", "exp": 1234567890}
        mock_decode.return_value = expected_payload
        
        result = _decode_token("valid_token")
        assert result == expected_payload
        mock_decode.assert_called_once()

    @patch('app.middleware.auth_middleware.decode')
    def test_decode_token_invalid(self, mock_decode):
        mock_decode.side_effect = InvalidTokenError("Invalid token")
        
        with pytest.raises(HTTPException) as exc_info:
            _decode_token("invalid_token")

        mock_decode.assert_called_once_with(
            "invalid_token",
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)

class TestVerifyToken:
    @patch('app.middleware.auth_middleware._decode_token')
    def test_verify_token_valid(self, mock_decode_token):
        credentials = MagicMock()
        credentials.credentials = "valid_token"
        expected_payload = {"sub": "user", "exp": 1234567890}
        mock_decode_token.return_value = expected_payload
        
        result = verify_token(credentials)
        assert result == expected_payload
        mock_decode_token.assert_called_once_with("valid_token")

    @pytest.mark.parametrize("test_input,expected_message", [
        (None, "Token required"),
        (MagicMock(credentials=""), "Invalid token")
    ])
    def test_verify_token_invalid_credentials(self, test_input, expected_message):
        with pytest.raises(HTTPException) as exc_info:
            verify_token(test_input)
        assert exc_info.value.status_code == 401
        assert expected_message in str(exc_info.value.detail)

class TestVerifyTokenOptional:
    @patch('app.middleware.auth_middleware._decode_token')
    def test_verify_token_optional_valid(self, mock_decode_token):
        credentials = MagicMock()
        credentials.credentials = "valid_token"
        expected_payload = {"sub": "user", "exp": 1234567890}
        mock_decode_token.return_value = expected_payload
        
        result = verify_token_optional(credentials)
        assert result == expected_payload
        mock_decode_token.assert_called_once_with("valid_token")

    @pytest.mark.parametrize("credentials", [
        None,
        MagicMock(credentials="")
    ])
    def test_verify_token_optional_none_or_empty(self, credentials):
        assert verify_token_optional(credentials) is None