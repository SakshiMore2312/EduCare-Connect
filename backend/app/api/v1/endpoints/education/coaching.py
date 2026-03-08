from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.education.review import Review
from app.schemas.education.review import ReviewCreate, ReviewResponse

from app.core.logger import logger
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.education.coaching import Coaching, CoachingType
from app.schemas.education.coaching import (
    CoachingCreate,
    CoachingUpdate,
    CoachingResponse
)
from app.api.v1.endpoints.deps import get_current_user, require_roles
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/coaching",
    tags=["Coaching"]
)

# ------------------- GET ALL -------------------
@router.get("/", response_model=List[CoachingResponse])
async def get_coaching_classes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    coaching_classes = db.query(Coaching).offset(skip).limit(limit).all()
    return coaching_classes

# ------------------- GET ONE -------------------
@router.get("/{coaching_id}", response_model=CoachingResponse)
async def get_coaching_class(
    coaching_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    coaching = db.query(Coaching).filter(Coaching.id == coaching_id).first()

    if not coaching:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coaching class not found"
        )
    return coaching

# ------------------- CREATE -------------------
@router.post("/", response_model=CoachingResponse, status_code=status.HTTP_201_CREATED)
async def create_coaching_class(
    coaching_data: CoachingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    # Check duplicate name
    existing_coaching = db.query(Coaching).filter(Coaching.name == coaching_data.name).first()
    if existing_coaching:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coaching class with this name already exists"
        )

    coaching_dict = jsonable_encoder(coaching_data)

    # Convert coaching_type string → Enum
    if coaching_dict.get("coaching_type"):
        try:
            coaching_dict["coaching_type"] = CoachingType(coaching_dict["coaching_type"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coaching type"
            )

    coaching = Coaching(**coaching_dict)
    db.add(coaching)
    db.commit()
    db.refresh(coaching)

    return coaching

# ------------------- UPDATE -------------------
@router.patch("/{coaching_id}", response_model=CoachingResponse)
async def update_coaching_class(
    coaching_id: int,
    coaching_data: CoachingUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    coaching = db.query(Coaching).filter(Coaching.id == coaching_id).first()

    if not coaching:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coaching class not found"
        )

    update_data = jsonable_encoder(coaching_data, exclude_unset=True)

    # Check for duplicate name
    if "name" in update_data and update_data["name"] != coaching.name:
        dup = db.query(Coaching).filter(Coaching.name == update_data["name"]).first()
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coaching class with this name already exists"
            )

    # Enum conversion
    if "coaching_type" in update_data:
        try:
            update_data["coaching_type"] = CoachingType(update_data["coaching_type"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coaching type"
            )

    for key, value in update_data.items():
        setattr(coaching, key, value)

    db.commit()
    db.refresh(coaching)
    return coaching

# ------------------- DELETE -------------------
@router.delete("/{coaching_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coaching_class(
    coaching_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_roles(["ADMIN"]))
):
    coaching = db.query(Coaching).filter(Coaching.id == coaching_id).first()

    if not coaching:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coaching class not found"
        )

    db.delete(coaching)
    db.commit()
    return None


# ------------------- REVIEWS -------------------
@router.get("/{coaching_id}/reviews", response_model=List[ReviewResponse])
async def get_coaching_reviews(
    coaching_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter(
        Review.coaching_id == coaching_id, Review.is_active == True
    ).offset(skip).limit(limit).all()
    return reviews


@router.post("/{coaching_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_coaching_review(
    coaching_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    entity = db.query(Coaching).filter(Coaching.id == coaching_id).first()
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coaching not found")
        
    review_dict = review_data.model_dump()
    review_dict["user_id"] = current_user.id
    review_dict["coaching_id"] = coaching_id
    
    review = Review(**review_dict)
    db.add(review)
    db.commit()
    db.refresh(review)
    
    logger.info(f"Review added to Coaching {coaching_id} by user {current_user.id}")
    return review
