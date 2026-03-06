from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.education.mess import Mess, MessType
from app.schemas.education.mess import (
    MessCreate,
    MessUpdate,
    MessResponse
)
from app.api.v1.endpoints.deps import get_current_user, require_roles
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/mess",
    tags=["Mess"]
)

# ------------------- GET ALL -------------------
@router.get("/", response_model=List[MessResponse])
def get_mess_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    mess_list = db.query(Mess).offset(skip).limit(limit).all()
    return mess_list

# ------------------- GET ONE -------------------
@router.get("/{mess_id}", response_model=MessResponse)
def get_mess(
    mess_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    mess = db.query(Mess).filter(Mess.id == mess_id).first()

    if not mess:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mess not found"
        )
    return mess

# ------------------- CREATE -------------------
@router.post("/", response_model=MessResponse, status_code=status.HTTP_201_CREATED)
def create_mess(
    mess_data: MessCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    # Check duplicate name
    existing_mess = db.query(Mess).filter(Mess.name == mess_data.name).first()
    if existing_mess:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess with this name already exists"
        )

    mess_dict = jsonable_encoder(mess_data)

    # Convert meal_types string → Enum
    if mess_dict.get("meal_types"):
        try:
            mess_dict["meal_types"] = MessType(mess_dict["meal_types"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid meal type"
            )

    mess = Mess(**mess_dict)
    db.add(mess)
    db.commit()
    db.refresh(mess)

    return mess

# ------------------- UPDATE -------------------
@router.patch("/{mess_id}", response_model=MessResponse)
def update_mess(
    mess_id: int,
    mess_data: MessUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    mess = db.query(Mess).filter(Mess.id == mess_id).first()

    if not mess:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mess not found"
        )

    update_data = jsonable_encoder(mess_data, exclude_unset=True)

    # Check for duplicate name
    if "name" in update_data and update_data["name"] != mess.name:
        dup = db.query(Mess).filter(Mess.name == update_data["name"]).first()
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mess with this name already exists"
            )

    # Enum conversion
    if "meal_types" in update_data:
        try:
            update_data["meal_types"] = MessType(update_data["meal_types"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid meal type"
            )

    for key, value in update_data.items():
        setattr(mess, key, value)

    db.commit()
    db.refresh(mess)
    return mess

# ------------------- DELETE -------------------
@router.delete("/{mess_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mess(
    mess_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    mess = db.query(Mess).filter(Mess.id == mess_id).first()

    if not mess:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mess not found"
        )

    db.delete(mess)
    db.commit()
    return None
