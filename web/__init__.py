from fastapi import APIRouter
from web import (
    index
)


router = APIRouter()


router.include_router(index.router)