from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db_dw
from ...models.data_warehouse_models import DimensionPedido
from ...schemas.data_warehouse_schemas import DimensionPedidoSchema

router = APIRouter()


@router.get("/", response_model=list[DimensionPedidoSchema])
def read_dimension_pedidos(db: Session = Depends(get_db_dw)):
    pedidos = db.query(DimensionPedido).all()
    return pedidos


@router.get("/{pedidoId}", response_model=DimensionPedidoSchema)
def read_dimension_pedido(pedidoId: int, db: Session = Depends(get_db_dw)):
    pedido = db.query(DimensionPedido).filter(
        DimensionPedido.PedidoId == pedidoId).first()
    if not pedido:
        raise HTTPException(
            status_code=404, detail="DimensionPedido not found")
    return pedido


@router.post("/", response_model=DimensionPedidoSchema)
def create_dimension_pedido(pedido: DimensionPedidoSchema, db: Session = Depends(get_db_dw)):
    new_pedido = DimensionPedido(**pedido.dict())
    db.add(new_pedido)
    db.commit()
    db.refresh(new_pedido)
    return new_pedido


@router.put("/{pedidoId}", response_model=DimensionPedidoSchema)
def update_dimension_pedido(pedidoId: int, pedido: DimensionPedidoSchema, db: Session = Depends(get_db_dw)):
    db_pedido = db.query(DimensionPedido).filter(
        DimensionPedido.PedidoId == pedidoId).first()
    if not db_pedido:
        raise HTTPException(
            status_code=404, detail="DimensionPedido not found")
    for var, value in pedido.dict().items():
        setattr(db_pedido, var, value)
    db.commit()
    return db_pedido


@router.delete("/{pedidoId}", status_code=204)
def delete_dimension_pedido(pedidoId: int, db: Session = Depends(get_db_dw)):
    db_pedido = db.query(DimensionPedido).filter(
        DimensionPedido.PedidoId == pedidoId).first()
    if not db_pedido:
        raise HTTPException(
            status_code=404, detail="DimensionPedido not found")
    db.delete(db_pedido)
    db.commit()
    return {"ok": True}
