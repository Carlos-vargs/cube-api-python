from fastapi import APIRouter
from .endpoints.dw_dimension_pedido import router as dimension_pedido_router

api_router = APIRouter()
api_router.include_router(dimension_pedido_router,
                          prefix="/dimension-pedido", tags=["DimensionPedido"])
