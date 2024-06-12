from fastapi import FastAPI
from .api.router import api_router
from app.api.endpoints.dw_dimension_cliente import router as cliente_router


app = FastAPI(title="API del Data Warehouse de TecnoNic")

app.include_router(api_router)

app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Data Warehouse API"}
