from fastapi import APIRouter
from .endpoints.eda import router as eda

api_router = APIRouter()
api_router.include_router(eda, prefix="/eda", tags=["eda"])
