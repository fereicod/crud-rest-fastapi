from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminBase(BaseModel):
    username: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(AdminBase):
    pass

class Admin(AdminBase):
    id: int