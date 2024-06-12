from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DimensionPedidoSchema(BaseModel):
    PedidoKey: Optional[int] = None
    SourceKey: str
    MetodoPago: str = 'Unknown'
    DireccionPago: str = 'Unknown'
    PrecioUnitario: float
    Cantidad: int
    Estado: str = 'Unknown'
    FechaPedido: datetime 
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class DimensionUbicacionSchema(BaseModel):
    UbicacionKey: Optional[int] = None
    SourceKey: str
    DireccionEnvio: str = 'Unknown'
    EstadoEnvio: str = 'Unknown'
    PaisEnvio: str = 'Unknown'
    CiudadEnvio: str = 'Unknown'
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class DimensionClienteSchema(BaseModel):
    ClienteKey: Optional[int] = None
    SourceKey: str
    Nombre: str = 'Unknown'
    Apellido: str = 'Unknown'
    Email: str = 'Unknown'
    Telefono: str = 'Unknown'
    Direccion: str = 'Unknown'
    Ciudad: str = 'Unknown'
    Pais: str = 'Unknown'
    Estado: str = 'Unknown'
    CodigoPostal: int
    PuntosFidelidad: int
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class DimensionOfertasSchema(BaseModel):
    OfertaKey: Optional[int] = None
    SourceKey: str
    Nombre: str = 'Unknown'
    Descripcion: str = 'Unknown'
    Descuento: float
    CodDescuento: int
    FechaLanzamiento: datetime 
    FechaCaducidad: datetime 
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class DimensionAreaEnvioSchema(BaseModel):
    AreaEnvioKey: Optional[int] = None
    SourceKey: str
    Area: str = 'Unknown'
    CostoEnvio: float
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class DimensionProductoSchema(BaseModel):
    ProductoKey: Optional[int] = None
    SourceKey: str
    Nombre: str = 'Unknown'
    FechaAgregado: datetime 
    Dimensiones: str = 'Unknown'
    Peso: float
    NombreCategoria: str = 'Unknown'
    NombreMarca: str = 'Unknown'
    ValidFrom: datetime 
    ValidTo: datetime 
    LineageKey: int

    class Config:
        orm_mode = True

class FactEnvioSchema(BaseModel):
    EnvioKey: Optional[int] = None
    PedidoKey: int
    OfertaKey: int
    AreaEnvioKey: int
    ClienteKey: int
    ProductoKey: int
    UbicacionKey: int
    EmpresaEnvio: str = 'Unknown'
    MetodoEnvio: str = 'Unknown'
    FechaEnvio: datetime 
    FechaEntrega: datetime 
    SourcePedidoKey: int
    LineageKey: int

    class Config:
        orm_mode = True
