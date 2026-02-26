from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.education.hostel import GenderType, RoomType

class HostelBase(BaseModel):
    name: str
    gender_type: GenderType
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    google_maps_link: Optional[str] = None
    room_type: RoomType
    facilities_available: Optional[str] = None
    mess_available: Optional[bool] = False
    monthly_rent: int
    security_features: Optional[str] = None
    reviews: Optional[str] = None

class HostelCreate(HostelBase):
    pass

class HostelUpdate(BaseModel):
    name: Optional[str] = None
    gender_type: Optional[GenderType] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    google_maps_link: Optional[str] = None
    room_type: Optional[RoomType] = None
    facilities_available: Optional[str] = None
    mess_available: Optional[bool] = None
    monthly_rent: Optional[int] = None
    security_features: Optional[str] = None
    reviews: Optional[str] = None

class HostelResponse(HostelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)