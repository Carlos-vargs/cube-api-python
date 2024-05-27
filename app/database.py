from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Importar variables de entorno
load_dotenv()

# Conexión para el Data Warehouse
DATABASE_URL_DW = os.getenv("DATA_WAREHOUSE_DATABASE_URL")
if not DATABASE_URL_DW:
    raise ValueError(
        "No DATA_WAREHOUSE_DATABASE URL provided in environment variables.")
engine_dw = create_engine(DATABASE_URL_DW)
SessionLocalDW = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_dw)

# Conexión para el CMI
DATABASE_URL_CMI = os.getenv("CMI_DATABASE_URL")
if not DATABASE_URL_CMI:
    raise ValueError("No CMI DATABASE URL provided in environment variables.")
engine_cmi = create_engine(DATABASE_URL_CMI)
SessionLocalCMI = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_cmi)

Base = declarative_base()


def get_db_dw():
    db = SessionLocalDW()
    try:
        yield db
    finally:
        db.close()


def get_db_cmi():
    db = SessionLocalCMI()
    try:
        yield db
    finally:
        db.close()
