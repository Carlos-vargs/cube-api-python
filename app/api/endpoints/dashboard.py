import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, HTTPException, Query
from app.database import get_db_dw
from sqlalchemy import func, extract
from fastapi.responses import JSONResponse
from io import BytesIO
from ...models.data_warehouse_models import (
    FactEnvio, DimPedido, DimCliente, DimOfertas, DimAreaEnvio, DimProducto, DimUbicacion
)
from datetime import datetime


router = APIRouter()


@router.get("/counters", response_model=dict)
def count_pedidos_by_estado(
        tab: str = Query(None, regex="^(yearly|monthly)$"),
        db: Session = Depends(get_db_dw)):
    current_year = datetime.now().year
    current_month = datetime.now().month
    estados = ["Entregado", "En ruta", "Pendiente", "Cancelado"]
    query = db.query(DimPedido.Estado, func.count(DimPedido.PedidoKey).label(
        'cantidad')).filter(DimPedido.Estado.in_(estados))

    if tab == "yearly":
        query = query.filter(
            extract('year', DimPedido.FechaPedido) == current_year)
        query = query.group_by(
            extract('year', DimPedido.FechaPedido), DimPedido.Estado)
        query = query.add_columns(
            extract('year', DimPedido.FechaPedido).label('Periodo'))
    elif tab == "monthly":
        query = query.filter(extract('month', DimPedido.FechaPedido) == current_month,
                             extract('year', DimPedido.FechaPedido) == current_year)
        query = query.group_by(
            extract('month', DimPedido.FechaPedido), DimPedido.Estado)
        query = query.add_columns(
            extract('month', DimPedido.FechaPedido).label('Periodo'))

    else:
        query = query.group_by(DimPedido.Estado)

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404, detail="No se encontraron pedidos")

    count_dict = {result.Estado: result.cantidad for result in results}

    return count_dict
