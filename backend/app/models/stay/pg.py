import enum
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base

class GenderType(str, enum.Enum):
    BOYS = "Boys"
    GIRLS = "Girls"
    CO_ED = "Co-ed"


class RoomType(str, enum.Enum):
    SINGLE = "Single"
    DOUBLE = "Double"
    TRIPLE = "Triple"

class PG(Base):
    __tablename__ = "pg"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    address = Column(Text, nullable=False)
    phone_number = Column(String(20))
    email = Column(String(255))
    google_maps_link = Column(Text)
    one_month_rent = Column(Integer, nullable=False)
    food_included = Column(Boolean, default=False)
    facilities_available = Column(Text)
    security_features = Column(Text)
    reviews = Column(Text)