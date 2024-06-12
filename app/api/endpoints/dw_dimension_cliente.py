from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db_dw
from ...models.data_warehouse_models import DimCliente
from ...schemas.data_warehouse_schemas import DimensionClienteSchema

router = APIRouter()


@router.get("/get", response_model=list)
def read_dimension_clientes(db: Session = Depends(get_db_dw)):
    clientes = db.query(DimCliente).all()
    return clientes


@router.get("/{ClienteKey}", response_model=DimensionClienteSchema)
def read_dimension_cliente(ClienteKey: int, db: Session = Depends(get_db_dw)):
    cliente = db.query(DimCliente).filter(DimCliente.ClienteKey == ClienteKey).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="DimCliente not found")
    return cliente


@router.post("/", response_model=DimensionClienteSchema)
def create_dimension_cliente(cliente: DimensionClienteSchema, db: Session = Depends(get_db_dw)):
    new_cliente = DimCliente(**cliente.dict())
    db.add(new_cliente)
    db.commit()
    db.refresh(new_cliente)
    return new_cliente


@router.put("/{ClienteKey}", response_model=DimensionClienteSchema)
def update_dimension_cliente(ClienteKey: int, cliente: DimensionClienteSchema, db: Session = Depends(get_db_dw)):
    db_cliente = db.query(DimCliente).filter(DimCliente.ClienteKey == ClienteKey).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="DimCliente not found")
    for var, value in cliente.dict().items():
        setattr(db_cliente, var, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.delete("/{ClienteKey}", status_code=204)
def delete_dimension_cliente(ClienteKey: int, db: Session = Depends(get_db_dw)):
    db_cliente = db.query(DimCliente).filter(DimCliente.ClienteKey == ClienteKey).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="DimCliente not found")
    db.delete(db_cliente)
    db.commit()
    return {"ok": True}
