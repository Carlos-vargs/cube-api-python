from fastapi import APIRouter
from .endpoints.eda import router as eda
from .endpoints.dashboard import router as dashboard

api_router = APIRouter()
api_router.include_router(eda, prefix="/eda", tags=["eda"])
api_router.include_router(
    dashboard, prefix="/bsc-dashboard", tags=["dashboard"])
