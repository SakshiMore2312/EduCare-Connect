from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints.education import colleges
from app.api.v1.endpoints.education import schools
from app.api.v1.endpoints.education import coaching
from app.api.v1.endpoints.education import mess


api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    colleges.router,
    prefix="/education/colleges",
    tags=["Colleges"]
)

api_router.include_router(
    schools.router,
    prefix="/education/schools",
    tags=["Schools"]
)

api_router.include_router(
    coaching.router,
    prefix="/education/coaching",
    tags=["Coaching"]
)

api_router.include_router(
    mess.router,
    prefix="/education/mess",
    tags=["Mess"]
)