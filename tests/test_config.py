import pytest
from pydantic_core import ValidationError
from app.core.config import Settings, validate_not_default

class TestValidateNotDefault:
    
    def test_valid_string(self):
        assert validate_not_default("valid_secret") == "valid_secret"
        assert validate_not_default("HS256") == "HS256"
        assert validate_not_default("30") == "30"
    
    @pytest.mark.parametrize("invalid_value", [
        "",
        "changethis", 
        "CHANGETHIS",
        "   ",
    ])
    def test_invalid_values_raise_error(self, invalid_value):
        with pytest.raises(ValueError, match="Value is missing or set to default"):
            validate_not_default(invalid_value)

class TestSettings:
    
    def test_settings_creation_with_valid_values(self):
        settings = Settings(
            JWT_SECRET="test_secret",
            JWT_ALGORITHM="HS256", 
            JWT_EXPIRE_MINUTES="20"
        )
        assert settings.JWT_SECRET == "test_secret"
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_EXPIRE_MINUTES == "20"
    
    @pytest.mark.parametrize("field,invalid_value", [
        ("JWT_SECRET", ""),
        ("JWT_SECRET", "changethis"),
        ("JWT_ALGORITHM", ""),
        ("JWT_ALGORITHM", "changethis"),
        ("JWT_EXPIRE_MINUTES", ""),
        ("JWT_EXPIRE_MINUTES", "changethis"),
    ])
    def test_settings_validation_fails(self, field, invalid_value):
        kwargs = {
            "JWT_SECRET": "valid_secret",
            "JWT_ALGORITHM": "HS256",
            "JWT_EXPIRE_MINUTES": "30"
        }
        kwargs[field] = invalid_value
        
        with pytest.raises(ValidationError):
            Settings(**kwargs)
