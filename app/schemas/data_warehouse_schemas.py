from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DimensionPedidoSchema(BaseModel):
    PedidoId: Optional[int] = None
    NombreMetodoPago: str = 'Unknown'
    DireccionPago: str = 'Unknown'
    PrecioUnitario: float
    Cantidad: int
    NombreEstado: str = 'Unknown'
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionUbicacionSchema(BaseModel):
    UbicacionId: Optional[int] = None
    DireccionEnvio: str = 'Unknown'
    EstadoEnvio: str = 'Unknown'
    PaisEnvio: str = 'Unknown'
    CiudadEnvio: str = 'Unknown'

    class Config:
        orm_mode = True


class DimensionTiempoSchema(BaseModel):
    DateId: Optional[int] = None
    FechaEnvio: datetime
    FechaEntrega: datetime
    FechaPedido: datetime
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionClienteSchema(BaseModel):
    ClienteId: Optional[int] = None
    Nombre: str = 'Unknown'
    Apellido: str = 'Unknown'
    Email: str = 'Unknown'
    Telefono: int
    Direccion: str = 'Unknown'
    Ciudad: str = 'Unknown'
    Pais: str = 'Unknown'
    Estado: str = 'Unknown'
    CodigoPostal: int
    PuntosFidelidad: int
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionOfertasSchema(BaseModel):
    Ofertasid: Optional[int] = None
    Nombre: str = 'Unknown'
    Descripcion: str = 'Unknown'
    Descuento: float
    CodDescuento: int
    FechaLanzamiento: datetime
    FechaCaducidad: datetime
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionAreaEnvioSchema(BaseModel):
    AreaEnvioId: Optional[int] = None
    NombreArea: str = 'Unknown'
    CostoEnvio: float
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionProductoSchema(BaseModel):
    ProductoId: Optional[int] = None
    Nombre: str = 'Unknown'
    FechaAgregado: datetime
    Dimensiones: str = 'Unknown'
    Peso: float
    Nombrecategoria: str = 'Unknown'
    NombreMarca: str = 'Unknown'
    FechaInicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class FactTableEnvioSchema(BaseModel):
    EnviosID: Optional[int] = None
    PedidoId: int
    OfertasId: int
    AreaEnvioId: int
    ClienteId: int
    ProductoId: int
    DATEKEY: int
    UbicacionId: int
    OfertasId: int
    EmpresaEnvio: str = 'Unknown'
    MetodoEnvio: str = 'Unknown'
    ValidFrom: datetime
    ValidTo: datetime

    class Config:
        orm_mode = True
