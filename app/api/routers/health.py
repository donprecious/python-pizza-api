from fastapi import APIRouter

from app.core.response import ok

router = APIRouter()


@router.get("/")
async def health_check():
    return ok({"status": "ok"})
