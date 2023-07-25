from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Magnus AI API"}


@router.get("/health")
async def health():
    return {"message": "OK"}
