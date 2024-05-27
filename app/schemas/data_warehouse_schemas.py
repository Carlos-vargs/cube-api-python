from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DimensionPedidoSchema(BaseModel):
    Pedidold: Optional[int] = None
    NombreMetodoPago: str = 'Unknown'
    DireccionPago: str = 'Unknown'
    PrecioUnitario: float
    Cantidad: int
    NombreEstado: str = 'Unknown'
    Fechalnicio: datetime
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
    Clienteld: Optional[int] = None
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
    Fechalnicio: datetime
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
    Fechalnicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionAreaEnvioSchema(BaseModel):
    AreaEnviold: Optional[int] = None
    NombreArea: str = 'Unknown'
    CostoEnvio: float
    Fechalnicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class DimensionProductoSchema(BaseModel):
    Productold: Optional[int] = None
    Nombre: str = 'Unknown'
    FechaAgregado: datetime
    Dimensiones: str = 'Unknown'
    Peso: float
    Nombrecategoria: str = 'Unknown'
    NombreMarca: str = 'Unknown'
    Fechalnicio: datetime
    FechaFin: datetime

    class Config:
        orm_mode = True


class FactTableEnvioSchema(BaseModel):
    EnviosID: Optional[int] = None
    Pedidold: int
    OfertasId: int
    AreaEnviold: int
    Clienteld: int
    Productold: int
    DATAKEY: int
    Ubicacionld: int
    Ofertasld: int
    EmpresaEnvio: str = 'Unknown'
    MetodoEnvio: str = 'Unknown'
    ValidFrom: datetime
    ValidTo: datetime

    class Config:
        orm_mode = True
