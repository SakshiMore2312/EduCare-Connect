from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.education.review import Review
from app.schemas.education.review import ReviewCreate, ReviewResponse

from app.core.logger import logger
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.education.schools import School, SchoolType, BoardType
from app.schemas.education.schools import (
    SchoolCreate,
    SchoolUpdate,
    SchoolResponse
)
from app.api.v1.endpoints.deps import get_current_user, require_roles
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/schools",
    tags=["Schools"]
)

# ------------------- GET ALL -------------------
@router.get("/", response_model=List[SchoolResponse])
async def get_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    schools = db.query(School).filter(School.is_active == True).offset(skip).limit(limit).all()
    return schools

# ------------------- GET ONE -------------------
@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    school = db.query(School).filter(School.id == school_id, School.is_active == True).first()

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return school

# ------------------- CREATE -------------------
@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: SchoolCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    # Check duplicate name
    existing_school = db.query(School).filter(School.name == school_data.name).first()
    if existing_school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School with this name already exists"
        )

    school_dict = jsonable_encoder(school_data)

    # Convert type string → Enum
    if school_dict.get("type"):
        try:
            school_dict["type"] = SchoolType(school_dict["type"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid school type"
            )

    if school_dict.get("board"):
        try:
            school_dict["board"] = BoardType(school_dict["board"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid board type"
            )

    school = School(**school_dict)
    db.add(school)
    db.commit()
    db.refresh(school)

    return school

# ------------------- UPDATE -------------------
@router.patch("/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    school = db.query(School).filter(School.id == school_id, School.is_active == True).first()

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )

    update_data = jsonable_encoder(school_data, exclude_unset=True)

    # Check for duplicate name
    if "name" in update_data and update_data["name"] != school.name:
        dup = db.query(School).filter(School.name == update_data["name"]).first()
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="School with this name already exists"
            )

    # Enum conversion
    if "type" in update_data:
        try:
            update_data["type"] = SchoolType(update_data["type"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid school type"
            )
    if "board" in update_data:
        try:
            update_data["board"] = BoardType(update_data["board"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid board type"
            )

    for key, value in update_data.items():
        setattr(school, key, value)

    db.commit()
    db.refresh(school)
    return school

# ------------------- DELETE -------------------
@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    school = db.query(School).filter(School.id == school_id, School.is_active == True).first()

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )

    # Soft delete
    school.is_active = False
    db.commit()
    return None

# ------------------- REVIEWS -------------------
@router.get("/{school_id}/reviews", response_model=List[ReviewResponse])
async def get_school_reviews(
    school_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter(
        Review.school_id == school_id, Review.is_active == True
    ).offset(skip).limit(limit).all()
    return reviews


@router.post("/{school_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_school_review(
    school_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    entity = db.query(School).filter(School.id == school_id).first()
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
        
    review_dict = review_data.model_dump()
    review_dict["user_id"] = current_user.id
    review_dict["school_id"] = school_id
    
    review = Review(**review_dict)
    db.add(review)
    db.commit()
    db.refresh(review)
    
    logger.info(f"Review added to School {school_id} by user {current_user.id}")
    return review
