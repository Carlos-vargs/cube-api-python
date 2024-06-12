from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, DECIMAL, NVARCHAR, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DimPedido(Base):
    __tablename__ = 'dim_Pedido'
    PedidoKey = Column('Pedido Key', Integer, primary_key=True, autoincrement=True)   
    SourceKey = Column('Source Key', NVARCHAR(50), nullable=False)
    MetodoPago = Column('Metodo Pago', NVARCHAR(100), default='Unknown')
    DireccionPago = Column('Direccion Pago', NVARCHAR(100), default='Unknown')
    PrecioUnitario = Column('Precio Unitario', DECIMAL(10, 2), nullable=False)
    Cantidad = Column('Cantidad', Integer, nullable=False)
    Estado = Column('Estado', NVARCHAR(100), default='Unknown')
    FechaPedido = Column('Fecha Pedido', DateTime, default=func.current_date())
    ValidFrom = Column('Valid From', DateTime, default=func.current_date())
    ValidTo = Column('Valid To', DateTime, default=func.current_date())
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class DimUbicacion(Base):
    __tablename__ = 'dim_Ubicacion'
    UbicacionKey = Column('Ubicacion Key', Integer, primary_key=True, autoincrement=True)
    SourceKey = Column('Source Key', NVARCHAR(50), nullable=False)
    DireccionEnvio = Column('Direccion Envio', NVARCHAR(100), default='Unknown')
    EstadoEnvio = Column('Estado Envio', NVARCHAR(100), default='Unknown')
    PaisEnvio = Column('Pais Envio', NVARCHAR(100), default='Unknown')
    CiudadEnvio = Column('Ciudad Envio', NVARCHAR(100), default='Unknown')
    ValidFrom = Column('Valid From', DateTime, default=func.current_date())
    ValidTo = Column('Valid To', DateTime, default=func.current_date())
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class DimCliente(Base):
    __tablename__ = 'dim_Cliente'
    
    ClienteKey = Column('Cliente Key', Integer, primary_key=True, autoincrement=True)
    SourceKey = Column('_Source Key', NVARCHAR(50), nullable=False)
    Nombre = Column('Nombre', NVARCHAR(100), default='Unknown')
    Apellido = Column('Apellido', NVARCHAR(100), default='Unknown')
    Email = Column('Email', NVARCHAR(100), default='Unknown')
    Telefono = Column('Telefono', NVARCHAR(100), default='Unknown')
    Direccion = Column('Direccion', NVARCHAR(100), default='Unknown')
    Ciudad = Column('Ciudad', NVARCHAR(100), default='Unknown')
    Pais = Column('Pais', NVARCHAR(100), default='Unknown')
    Estado = Column('Estado', NVARCHAR(100), default='Unknown')
    CodigoPostal = Column('Codigo Postal', Integer, nullable=False)
    PuntosFidelidad = Column('Puntos Fidelidad', Integer, nullable=False)
    ValidFrom = Column('Valid From', DateTime)
    ValidTo = Column('Valid To', DateTime)
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class DimOfertas(Base):
    __tablename__ = 'dim_Ofertas'
    OfertaKey = Column('Oferta Key', Integer, primary_key=True, autoincrement=True)
    SourceKey = Column('Source Key', NVARCHAR(50), nullable=False)
    Nombre = Column('Nombre', NVARCHAR(100), default='Unknown')
    Descripcion = Column('Descripcion', NVARCHAR(100), default='Unknown')
    Descuento = Column('Descuento', DECIMAL(10, 2), nullable=False)
    CodDescuento = Column('Cod Descuento', Integer, nullable=False)
    FechaLanzamiento = Column('Fecha Lanzamiento', DateTime, default=func.current_date())
    FechaCaducidad = Column('Fecha Caducidad', DateTime, default=func.current_date())
    ValidFrom = Column('Valid From', DateTime, default=func.current_date())
    ValidTo = Column('Valid To', DateTime, default=func.current_date())
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class DimAreaEnvio(Base):
    __tablename__ = 'dim_AreaEnvio'
    AreaEnvioKey = Column('Area Envio Key', Integer, primary_key=True, autoincrement=True)
    SourceKey = Column('Source Key', NVARCHAR(50), nullable=False)
    Area = Column('Area', NVARCHAR(100), default='Unknown')
    CostoEnvio = Column('Costo Envio', DECIMAL(10, 2), nullable=False)
    ValidFrom = Column('Valid From', DateTime, default=func.current_date())
    ValidTo = Column('Valid To', DateTime, default=func.current_date())
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class DimProducto(Base):
    __tablename__ = 'dim_Producto'
    ProductoKey = Column('Producto Key', Integer, primary_key=True, autoincrement=True)
    Nombre = Column('Nombre', NVARCHAR(100), default='Unknown')
    SourceKey = Column('Source Key', NVARCHAR(50), nullable=False)
    FechaAgregado = Column('Fecha Agregado', DateTime, default=func.current_date())
    Dimensiones = Column('Dimensiones', NVARCHAR(100), default='Unknown')
    Peso = Column('Peso', DECIMAL(10, 2), nullable=False)
    NombreCategoria = Column('Nombre Categoria', NVARCHAR(100), default='Unknown')
    NombreMarca = Column('Nombre Marca', NVARCHAR(100), default='Unknown')
    ValidFrom = Column('Valid From', DateTime, default=func.current_date())
    ValidTo = Column('Valid To', DateTime, default=func.current_date())
    LineageKey = Column('Lineage Key', Integer, nullable=False)

class FactEnvio(Base):
    __tablename__ = 'Fact_Envio'
    EnvioKey = Column('Envio Key', Integer, primary_key=True, autoincrement=True)
    PedidoKey = Column('Pedido Key', Integer, nullable=False)
    OfertaKey = Column('Oferta Key', Integer, nullable=False)
    AreaEnvioKey = Column('Area Envio Key', Integer, nullable=False)
    ClienteKey = Column('Cliente Key', Integer, nullable=False)
    ProductoKey = Column('Producto Key', Integer, nullable=False)
    UbicacionKey = Column('Ubicacion Key', Integer, nullable=False)
    EmpresaEnvio = Column('Empresa Envio', NVARCHAR(100), default='Unknown')
    MetodoEnvio = Column('Metodo Envio', NVARCHAR(100), default='Unknown')
    FechaEnvio = Column('Fecha Envio', DateTime, default=func.current_date())
    FechaEntrega = Column('Fecha Entrega', DateTime, default=func.current_date())
    SourcePedidoKey = Column('Source Pedido Key', Integer, nullable=False)
    LineageKey = Column('Lineage Key', Integer, nullable=False)
