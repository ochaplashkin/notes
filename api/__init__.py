from fastapi import APIRouter
from api import (
    system
)


router = APIRouter(prefix="/api")

router.include_router(system.router)