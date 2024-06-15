from fastapi import FastAPI
from .api.router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API del Data Warehouse de TecnoNic")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Data Warehouse API"}
