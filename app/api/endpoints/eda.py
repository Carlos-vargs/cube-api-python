import matplotlib.pyplot as plt
import io
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends,APIRouter,HTTPException
from ...models.data_warehouse_models import Base, DimPedido, DimUbicacion, DimCliente, DimOfertas, DimAreaEnvio, DimProducto, FactEnvio
from typing import List
import pandas as pd
from app.database import get_db_dw

router = APIRouter()

def getDataFrame(db: Session):
    result = db.query(
        FactEnvio.EnvioKey,
        DimPedido.MetodoPago,
        DimPedido.DireccionPago,
        DimPedido.PrecioUnitario,
        DimPedido.Cantidad,
        DimPedido.Estado,
        DimPedido.FechaPedido,
        DimCliente.Nombre,
        DimCliente.PuntosFidelidad,
        DimOfertas.Nombre.label('ofertas'),
        DimOfertas.Descuento,
        DimAreaEnvio.Area,
        DimAreaEnvio.CostoEnvio,
        DimProducto.Nombre.label('Producto'),
        DimProducto.NombreMarca,
        DimProducto.NombreCategoria,
        FactEnvio.EmpresaEnvio, 
        FactEnvio.MetodoEnvio,
        DimUbicacion.EstadoEnvio,
        DimUbicacion.CiudadEnvio.label('Ciudad'),
        FactEnvio.FechaEnvio,
        FactEnvio.FechaEntrega
    ).join(DimPedido, FactEnvio.PedidoKey == DimPedido.PedidoKey) \
     .join(DimCliente, FactEnvio.ClienteKey == DimCliente.ClienteKey) \
     .join(DimOfertas, FactEnvio.OfertaKey == DimOfertas.OfertaKey) \
     .join(DimAreaEnvio, FactEnvio.AreaEnvioKey == DimAreaEnvio.AreaEnvioKey) \
     .join(DimProducto, FactEnvio.ProductoKey == DimProducto.ProductoKey) \
     .join(DimUbicacion, FactEnvio.UbicacionKey == DimUbicacion.UbicacionKey).all()
    
    # Convertir los resultados a un DataFrame de pandas
    df = pd.DataFrame(result, columns=[
        'EnvioKey', 'MetodoPago', 'DireccionPago', 'PrecioUnitario', 'Cantidad', 'Estado', 
        'FechaPedido', 'Nombre', 'PuntosFidelidad', 'Nombre_ofertas', 'Descuento', 'Area', 
        'CostoEnvio', 'Nombre_producto', 'NombreMarca', 'NombreCategoria', 'EmpresaEnvio', 
        'MetodoEnvio', 'EstadoEnvio', 'Ciudad', 'FechaEnvio', 'FechaEntrega'
    ])
    return df


@router.get("/df", response_model=List)
def get_envios(db: Session = Depends(get_db_dw)):
    df = getDataFrame(db)
    return df.to_dict(orient='records')

@router.get("CuartaEtapa/Histograma")
async def get_Histograma():
    pass    


@router.get("CuartaEtapa/BoxPlot")
async def get_Histograma():
    pass

@router.get("CuartaEtapa/Z-score")
async def get_Histograma():
    pass


@router.get("QuintaEtapa/Correlacion")
async def get_Histograma():
    pass
    

@router.get("QuintaEtapa/scatter")
async def get_Histograma():
    pass
    
    
    
    
    
    
    
    
    
    
    
#     df = pd.DataFrame({
#     'x': range(10),
#     'y': [i**2 for i in range(10)]
#     })

#     # Crear el gráfico de barras
#     plt.figure()
#     df.plot(x='x', y='y', kind='bar')
#     plt.title("test")

#     # Guardar el gráfico en un buffer
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)

#     # Devolver la imagen como respuesta
#     return Response(content=buf.read(), media_type="image/png")

# # Ejecuta la aplicación con: uvicorn script_name:app --reload