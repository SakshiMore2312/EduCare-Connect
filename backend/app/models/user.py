from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    phone = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True)
    emergency_contact_1 = Column(String(20), nullable=True)
    emergency_contact_2 = Column(String(20), nullable=True)
    profile_image = Column(String(500), nullable=True)

    # Social Handles
    social_instagram = Column(String(255), nullable=True)
    social_linkedin = Column(String(255), nullable=True)
    social_github = Column(String(255), nullable=True)

    # Notification & Permission Settings
    push_notifications = Column(Boolean, nullable=False, default=True)

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.USER
    )

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )