from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints.education import colleges
from app.api.v1.endpoints.education import schools
from app.api.v1.endpoints.education import coaching
from app.api.v1.endpoints.education import mess
from app.api.v1.endpoints.stay import hostels
from app.api.v1.endpoints.stay import pg
from app.api.v1.endpoints.profile import profile


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

api_router.include_router(
    hostels.router,
    prefix="/stay/hostels",
    tags=["Hostels"]
)

api_router.include_router(
    pg.router,
    prefix="/stay/pgs",
    tags=["PGs"]
)

api_router.include_router(
    profile.router,
    prefix="/profile",
    tags=["Profile"]
)