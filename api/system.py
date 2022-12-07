from starlette.responses import JSONResponse
from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/health")
async def health() -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": True})