import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, HTTPException, Query
from app.database import get_db_dw
from sqlalchemy import func, extract, desc
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


def calculate_trend(current, previous):
    if current > previous:
        return 'up'
    elif current < previous:
        return 'down'
    return 'no change'  # No change


@router.get("/trends/states")
def state_trends(db: Session = Depends(get_db_dw)):
    # Obtener los dos meses más recientes
    recent_months = db.query(
        extract('year', FactEnvio.FechaEnvio).label('Year'),
        extract('month', FactEnvio.FechaEnvio).label('Month')
    ).distinct().order_by(desc('Year'), desc('Month')).limit(2).all()

    if len(recent_months) < 2:
        return {"message": "Insufficient data"}

    # Datos de los dos meses
    last_month = recent_months[1]
    current_month = recent_months[0]

    # Consultas para cada mes
    def get_month_data(year, month):
        return db.query(
            DimUbicacion.EstadoEnvio,
            func.count(FactEnvio.EnvioKey).label('TotalEnvios')
        ).join(FactEnvio, FactEnvio.UbicacionKey == DimUbicacion.UbicacionKey) \
         .filter(
             extract('year', FactEnvio.FechaEnvio) == year,
             extract('month', FactEnvio.FechaEnvio) == month
        ).group_by(DimUbicacion.EstadoEnvio).all()

    last_data = {item.EstadoEnvio: item.TotalEnvios for item in get_month_data(
        last_month.Year, last_month.Month)}
    current_data = {item.EstadoEnvio: item.TotalEnvios for item in get_month_data(
        current_month.Year, current_month.Month)}

    # Calcular tendencia
    response = []
    for state, total in current_data.items():
        previous_total = last_data.get(state, 0)
        trend = "up" if total > previous_total else "down" if total < previous_total else "no change"
        response.append({
            "EstadoEnvio": state,
            "TotalEnvios": total,
            "Trend": trend
        })

    return response


@router.get("/trends/clients")
def client_trends(db: Session = Depends(get_db_dw)):
    # Obtener los dos meses más recientes
    recent_months = db.query(
        extract('year', FactEnvio.FechaEnvio).label('Year'),
        extract('month', FactEnvio.FechaEnvio).label('Month')
    ).distinct().order_by(desc('Year'), desc('Month')).limit(2).all()

    if len(recent_months) < 2:
        return {"message": "Insufficient data"}

    # Datos de los dos meses
    last_month = recent_months[1]
    current_month = recent_months[0]

    # Consultas para cada mes
    def get_month_data(year, month):
        return db.query(
            DimCliente.ClienteKey,
            DimCliente.Nombre,
            func.count(FactEnvio.EnvioKey).label('TotalPedidos')
        ).join(FactEnvio, FactEnvio.ClienteKey == DimCliente.ClienteKey) \
         .filter(
             extract('year', FactEnvio.FechaEnvio) == year,
             extract('month', FactEnvio.FechaEnvio) == month
        ).group_by(DimCliente.ClienteKey, DimCliente.Nombre).all()

    last_data = {item.ClienteKey: item.TotalPedidos for item in get_month_data(
        last_month.Year, last_month.Month)}
    current_data = {(item.ClienteKey, item.Nombre): item.TotalPedidos for item in get_month_data(
        current_month.Year, current_month.Month)}

    response = []
    for (cliente, nombre), total in current_data.items():
        previous_total = last_data.get(cliente, 0)
        trend = "up" if total > previous_total else "down" if total < previous_total else "no change"
        response.append({
            "ClienteKey": cliente,
            "ClienteNombre": nombre,
            "TotalPedidos": total,
            "Trend": trend
        })

    return response
