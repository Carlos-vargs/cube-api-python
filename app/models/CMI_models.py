from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base() # no toque nada de conexión

class CMISet(Base):
    __tablename__ = 'CMISet'
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    TimePeriod = Column(DateTime, nullable=False)

    # definir relaciones ()
    objectives = relationship("ObjectiveSet", back_populates="cmi")


class ObjectiveSet(Base):
    __tablename__ = 'ObjectiveSet'
    Id = Column(Integer, primary_key=True, index=True)
    Description = Column(String, nullable=False)
    Metric = Column(String, nullable=False)
    Weighting = Column(DECIMAL, nullable=False)
    CMIId = Column(Integer, ForeignKey('CMISet.Id'), nullable=False)
    PerspectiveId = Column(Integer, ForeignKey('PerspectiveSet.Id'), nullable=False)

    cmi = relationship("CMISet", back_populates="objectives")
    perspective = relationship("PerspectiveSet", back_populates="objectives")
    indicators = relationship("IndicatorSet", back_populates="objective")


class PerspectiveSet(Base):
    __tablename__ = 'PerspectiveSet'
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)

    objectives = relationship("ObjectiveSet", back_populates="perspective")


class IndicatorSet(Base):
    __tablename__ = 'IndicatorSet'
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    MeasurementFrequency = Column(String, nullable=False)
    UnitMeasure = Column(String, nullable=False)
    ObjectiveId = Column(Integer, ForeignKey('ObjectiveSet.Id'), nullable=False)
    MetricTypeId = Column(Integer, ForeignKey('MetricTypeSet.Id'), nullable=False)

    objective = relationship("ObjectiveSet", back_populates="indicators")
    metric_type = relationship("MetricTypeSet", back_populates="indicators")
    data_indicators = relationship("DataIndicatorSet", back_populates="indicator")
    targets = relationship("TargetSet", back_populates="indicator")


class MetricTypeSet(Base):
    __tablename__ = 'MetricTypeSet'
    Id = Column(Integer, primary_key=True, index=True)

    indicators = relationship("IndicatorSet", back_populates="metric_type")


class DataIndicatorSet(Base):
    __tablename__ = 'DataIndicatorSet'
    Id = Column(Integer, primary_key=True, index=True)
    Value = Column(DECIMAL, nullable=False)
    Date = Column(DateTime, nullable=False)
    IndicatorId = Column(Integer, ForeignKey('IndicatorSet.Id'), nullable=False)

    indicator = relationship("IndicatorSet", back_populates="data_indicators")


class TargetSet(Base):
    __tablename__ = 'TargetSet'
    Id = Column(Integer, primary_key=True, index=True)
    Description = Column(String, nullable=False)
    ExpectedValue = Column(DECIMAL, nullable=False)
    DeadlineDate = Column(DateTime, nullable=False)
    IndicatorId = Column(Integer, ForeignKey('IndicatorSet.Id'), nullable=False)

    indicator = relationship("IndicatorSet", back_populates="targets")
