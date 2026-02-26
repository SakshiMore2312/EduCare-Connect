from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from typing import Optional

class PGBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    google_maps_link: Optional[HttpUrl] = None
    one_month_rent: int = Field(..., gt=0)
    food_included: Optional[bool] = False
    facilities_available: Optional[str] = None
    security_features: Optional[str] = None
    reviews: Optional[str] = None

class PGCreate(PGBase):
    pass

class PGUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    google_maps_link: Optional[HttpUrl] = None
    one_month_rent: Optional[int] = Field(None, gt=0)
    food_included: Optional[bool] = None
    facilities_available: Optional[str] = None
    security_features: Optional[str] = None
    reviews: Optional[str] = None

class PGResponse(PGBase):
    id: int

    model_config = ConfigDict(from_attributes=True)