import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response
from app.database import get_db_dw
from fastapi.responses import JSONResponse
from io import BytesIO
from ...models.data_warehouse_models import (
    FactEnvio, DimPedido, DimCliente, DimOfertas, DimAreaEnvio, DimProducto, DimUbicacion
)
from datetime import datetime


router = APIRouter()


def queryData(db: Session):
    return db.query(
        FactEnvio.EnvioKey.label('Envio Key'),
        (DimCliente.Nombre + " " + DimCliente.Apellido).label('Full Name'),
        DimCliente.PuntosFidelidad.label('Puntos de fidelidad'),
        FactEnvio.EmpresaEnvio.label('Empresa Envio'),
        DimAreaEnvio.Area,
        FactEnvio.MetodoEnvio.label('Metodo Envio'),
        DimAreaEnvio.CostoEnvio.label('Costo Envio'),
        DimProducto.Nombre.label('Producto'),
        DimPedido.PrecioUnitario.label('Precio Unitario'),
        DimPedido.Cantidad,
        DimPedido.MetodoPago.label('Metodo Pago'),
        DimOfertas.Nombre.label('Oferta'),
        DimOfertas.Descuento,
    ).join(DimPedido, FactEnvio.PedidoKey == DimPedido.PedidoKey) \
     .join(DimCliente, FactEnvio.ClienteKey == DimCliente.ClienteKey) \
     .join(DimOfertas, FactEnvio.OfertaKey == DimOfertas.OfertaKey) \
     .join(DimAreaEnvio, FactEnvio.AreaEnvioKey == DimAreaEnvio.AreaEnvioKey) \
     .join(DimProducto, FactEnvio.ProductoKey == DimProducto.ProductoKey) \
     .join(DimUbicacion, FactEnvio.UbicacionKey == DimUbicacion.UbicacionKey).all()


def createDataframe(result):
    df = pd.DataFrame(result).set_index("Envio Key")
    df['Costo Envio'] = pd.to_numeric(df['Costo Envio'], errors='coerce')
    df['Precio Unitario'] = pd.to_numeric(
        df['Precio Unitario'], errors='coerce')
    df['Descuento'] = pd.to_numeric(df['Descuento'], errors='coerce')

    df['Area'] = df['Area'].astype('category')
    df['Producto'] = df['Producto'].astype('category')
    df['Metodo Pago'] = df['Metodo Pago'].astype('category')
    df['Oferta'] = df['Oferta'].astype('category')

    df['Costo Final'] = (
        (df['Cantidad'] * df['Precio Unitario'] +
         df['Costo Envio']) * (1 - df['Descuento'] / 100)
    ).round(2)

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    return df


def getDataFrame(db: Session):
    result = queryData(db)
    return createDataframe(result)


@router.get("/df/test-schema")
def dfTest(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    print(df.dtypes)
    return {"message": "Test result printed in the terminal"}


@router.get("/df", response_model=list)
def ViewDf(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    return df.to_dict(orient='records')


@router.get("/histograma-costo-envio")
async def get_sdchistograma(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    data = df['Costo Envio'].to_list()
    # https://www.highcharts.com/demo/highcharts/histogram
    return JSONResponse(content=data)


@router.get("/box-plot")
async def get_boxplot(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)

    columns = ['Costo Final', 'Descuento',
               'Cantidad', 'Costo Envio', 'Precio Unitario']
    data = {}

    for column in columns:
        if column in df:
            values = df[column]

            min_val = np.min(values).item()
            q1 = np.percentile(values, 25).item()
            median = np.percentile(values, 50).item()
            q3 = np.percentile(values, 75).item()
            max_val = np.max(values).item()
            mean_val = np.mean(values).item()

            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = values[(values < lower_bound) |
                              (values > upper_bound)].tolist()

            data[column] = {
                "boxplot": [min_val, q1, median, q3, max_val],
                "mean": mean_val,
                "outliers": [[0, outlier] for outlier in outliers]
            }
            # https://www.highcharts.com/demo/highcharts/box-plot 

    return JSONResponse(content=data)


@router.get("/scatter-descuento")
async def get_scatter_descuento(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)

    descuento = df['Descuento'].to_list()

    data = [[i, val] for i, val in enumerate(descuento)]
    # https://www.highcharts.com/demo/highcharts/scatter
    return JSONResponse(content=data)


@router.get("/scatter-costo-final")
async def get_scatter_costo_final(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)

    CoastFinal = df['Costo Final'].to_list()

    data = [[i, val] for i, val in enumerate(CoastFinal)]
    # https://www.highcharts.com/demo/highcharts/scatter
    return JSONResponse(content=data)


@router.get("/heat-map")
async def get_heat_map(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    heatmap_data = df[['Puntos de fidelidad', 'Costo Envio',
                       'Precio Unitario', 'Cantidad', 'Descuento', 'Costo Final']]

    correlation_matrix = heatmap_data.corr()
    heatmapJson = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            heatmapJson.append([i, j, correlation_matrix.iat[i, j]])

        # https://www.highcharts.com/demo/highcharts/heatmap

    return JSONResponse(content={
        "xAxisCategories": correlation_matrix.columns.tolist(),
        "yAxisCategories": correlation_matrix.index.tolist(),
        "heatmapData": heatmapJson
    })


@router.get("/correlation")
async def get_correlation(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    contingency_table = pd.crosstab(df['Producto'], df['Area'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    heatmapJson = []
    for i in range(len(contingency_table.index)):
        for j in range(len(contingency_table.columns)):
            heatmapJson.append(
                [int(i), int(j), int(contingency_table.iat[i, j])])

    # https://www.highcharts.com/demo/highcharts/heatmap

    return JSONResponse(content={
        "xAxisCategories": contingency_table.columns.astype(str).tolist(),
        "yAxisCategories": contingency_table.index.astype(str).tolist(),
        "heatmapData": heatmapJson
    })


@router.get("/describe", response_model=list)
async def get_describe(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    description = df.describe(include='all').reset_index()
    description_list = description.to_dict(orient='records')

    for record in description_list:
        for key, value in record.items():
            if isinstance(value, (pd.Timestamp, datetime)):
                record[key] = value.isoformat() if pd.notnull(value) else None
            elif pd.isna(value):
                record[key] = None
    
    return description_list

@router.get("/head")
async def get_head(db: Session = Depends(get_db_dw)):
    pass


@router.get("/tail")
async def get_tail(db: Session = Depends(get_db_dw)):
    pass

@router.get("/tabla-contigencia")
async def get_tail(db: Session = Depends(get_db_dw)):
    pass
