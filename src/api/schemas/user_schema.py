from api.schemas.core.schema import Schema
from typing import Optional


class UserSchema(Schema):
    full_name: str
    email: str
    password:str

class UserUpdateSchema(Schema):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserLogginSchema(Schema):
    full_name: str
    email: str