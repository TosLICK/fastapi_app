from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SightseeingModel(BaseModel):
    name: str
    location: str
    description: Optional[str] = None


class SightseeingUpdateModel(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class SightseeingResponse(SightseeingModel):
    id: int

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6)


class UserDB(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserDB
    detail: str = "User created successfully"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
