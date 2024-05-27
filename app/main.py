from fastapi import FastAPI
from .api.router import api_router

app = FastAPI(title="API del Data Warehouse de TecnoNic")

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Data Warehouse API"}
