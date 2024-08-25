from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

class UserProfile(UserBase):
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
