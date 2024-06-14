import pandas as pd
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats  # For handling outliers
from fastapi import APIRouter, Depends, Response
from app.database import get_db_dw
from io import BytesIO
from ...models.data_warehouse_models import (
    FactEnvio, DimPedido, DimCliente, DimOfertas, DimAreaEnvio, DimProducto, DimUbicacion
)

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
    df['Precio Unitario'] = pd.to_numeric(df['Precio Unitario'], errors='coerce')
    df['Descuento'] = pd.to_numeric(df['Descuento'], errors='coerce')
    
    df['Area'] = df['Area'].astype('category')
    df['Producto'] = df['Producto'].astype('category')
    df['Metodo Pago'] = df['Metodo Pago'].astype('category') 
    df['Oferta'] = df['Oferta'].astype('category')
    
    df['Costo Final'] = (
        (df['Cantidad'] * df['Precio Unitario'] + df['Costo Envio']) * (1 - df['Descuento'] / 100)
    ).round(2)

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    return df

def getDataFrame(db: Session):
    result = queryData(db)
    return createDataframe(result)

def plotToResponse(plotFunc):
    buf = BytesIO()
    plotFunc(buf)
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")

@router.get("/df/test")
def dfTest(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    return print(df.dtypes)

@router.get("/df", response_model=list)
def ViewDf(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    return df.to_dict(orient='records')

@router.get("/Histograma")
def get_histograma(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Costo Envio'], kde=True)
    plt.title('Histograma de Costo Envio')
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))

@router.get("/Box-Plot")
def get_boxplot(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['Costo Final'])
    plt.title('Boxplot de Costo Final')
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))

@router.get("/Scatter-Costo-Envio")
def get_scatter_costo_envio(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df.index, y=df['Costo Envio'])
    plt.xlabel('Envio Key')
    plt.ylabel('Costo Envio')
    plt.title('Scatter Plot of Costo Envio')
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))

@router.get("/Scatter-Costo-Final")
def get_scatter_costo_final(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df.index, y=df['Costo Final'])
    plt.xlabel('Envio Key')
    plt.ylabel('Costo Final')
    plt.title('Scatter Plot of Costo Final')
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))

@router.get("/heat-map")
def get_heat_map(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[['Puntos de fidelidad', 'Costo Envio', 'Precio Unitario', 'Cantidad', 'Descuento', 'Costo Final']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Pearson's Correlation Heat Map")
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))

@router.get("/Correlation")
def get_correlation(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    
    contingency_table = pd.crosstab(df['Producto'], df['Area'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    plt.figure(figsize=(14, 10))
    sns.heatmap(contingency_table, annot=True, cmap='coolwarm', linewidths=0.5, fmt='d')
    plt.title('Tabla de Contingencia entre Producto y Area')
    
    return plotToResponse(lambda buf: plt.savefig(buf, format='png'))
