from sqlalchemy import Column, Integer, String, Float, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DimensionPedido(Base):
    __tablename__ = 'DimensionPedido'
    Pedidold = Column(Integer, primary_key=True, autoincrement=True)
    NombreMetodoPago = Column(String(100), default='Unknown')
    DireccionPago = Column(String(100), default='Unknown')
    PrecioUnitario = Column(DECIMAL(10, 2), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    NombreEstado = Column(String(100), default='Unknown')
    Fechalnicio = Column(DateTime)
    FechaFin = Column(DateTime)


class DimensionUbicacion(Base):
    __tablename__ = 'DimensionUbicacion'
    UbicacionId = Column(Integer, primary_key=True, autoincrement=True)
    DireccionEnvio = Column(String(100), default='Unknown')
    EstadoEnvio = Column(String(100), default='Unknown')
    PaisEnvio = Column(String(100), default='Unknown')
    CiudadEnvio = Column(String(100), default='Unknown')


class DimensionTiempo(Base):
    __tablename__ = 'DimensionTiempo'
    DateId = Column(Integer, primary_key=True, autoincrement=True)
    FechaEnvio = Column(DateTime)
    FechaEntrega = Column(DateTime)
    FechaPedido = Column(DateTime)
    FechaInicio = Column(DateTime)
    FechaFin = Column(DateTime)


class DimensionCliente(Base):
    __tablename__ = 'DimensionCliente'
    Clienteld = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), default='Unknown')
    Apellido = Column(String(100), default='Unknown')
    Email = Column(String(100), default='Unknown')
    Telefono = Column(Integer, nullable=False)
    Direccion = Column(String(100), default='Unknown')
    Ciudad = Column(String(100), default='Unknown')
    Pais = Column(String(100), default='Unknown')
    Estado = Column(String(100), default='Unknown')
    CodigoPostal = Column(Integer, nullable=False)
    PuntosFidelidad = Column(Integer, nullable=False)
    Fechalnicio = Column(DateTime)
    FechaFin = Column(DateTime)


class DimensionOfertas(Base):
    __tablename__ = 'DimensionOfertas'
    Ofertasid = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), default='Unknown')
    Descripcion = Column(String(100), default='Unknown')
    Descuento = Column(DECIMAL(10, 2), nullable=False)
    CodDescuento = Column(Integer, nullable=False)
    FechaLanzamiento = Column(DateTime)
    FechaCaducidad = Column(DateTime)
    Fechalnicio = Column(DateTime)
    FechaFin = Column(DateTime)


class DimensionAreaEnvio(Base):
    __tablename__ = 'DimensionAreaEnvio'
    AreaEnviold = Column(Integer, primary_key=True, autoincrement=True)
    NombreArea = Column(String(100), default='Unknown')
    CostoEnvio = Column(DECIMAL(10, 2), nullable=False)
    Fechalnicio = Column(DateTime)
    FechaFin = Column(DateTime)


class DimensionProducto(Base):
    __tablename__ = 'DimensionProducto'
    Productold = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), default='Unknown')
    FechaAgregado = Column(DateTime)
    Dimensiones = Column(String(100), default='Unknown')
    Peso = Column(DECIMAL(10, 2), nullable=False)
    Nombrecategoria = Column(String(100), default='Unknown')
    NombreMarca = Column(String(100), default='Unknown')
    Fechalnicio = Column(DateTime)
    FechaFin = Column(DateTime)


class FactTableEnvio(Base):
    __tablename__ = 'FactTableEnvio'
    EnviosID = Column(Integer, primary_key=True, autoincrement=True)
    Pedidold = Column(Integer, ForeignKey('DimensionPedido.Pedidold'))
    OfertasId = Column(Integer, ForeignKey('DimensionOfertas.Ofertasid'))
    AreaEnviold = Column(Integer, ForeignKey('DimensionAreaEnvio.AreaEnviold'))
    Clienteld = Column(Integer, ForeignKey('DimensionCliente.Clienteld'))
    Productold = Column(Integer, ForeignKey('DimensionProducto.Productold'))
    DATAKEY = Column(Integer, ForeignKey('DimensionTiempo.DateId'))
    Ubicacionld = Column(Integer, ForeignKey('DimensionUbicacion.UbicacionId'))
    Ofertasld = Column(Integer, ForeignKey('DimensionOfertas.Ofertasid'))
    EmpresaEnvio = Column(String(100), default='Unknown')
    MetodoEnvio = Column(String(100), default='Unknown')
    ValidFrom = Column(DateTime)
    ValidTo = Column(DateTime)
