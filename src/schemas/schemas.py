from typing import Optional

from pydantic import BaseModel


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