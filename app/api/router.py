from fastapi import APIRouter
from .endpoints.dw_dimension_cliente import router as dimension_cliente_router

api_router = APIRouter()
api_router.include_router(dimension_cliente_router,
                          prefix="/clientes", tags=["clientes"])
