from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CMISetSchema(BaseModel):
    Id: Optional[int] = None
    Name: str
    TimePeriod: datetime

    class Config:
        orm_mode = True


class ObjectiveSetSchema(BaseModel):
    Id: Optional[int] = None
    Description: str
    Metric: str
    Weighting: float
    CMIId: int
    PerspectiveId: int

    class Config:
        orm_mode = True


class PerspectiveSetSchema(BaseModel):
    Id: Optional[int] = None
    Name: str

    class Config:
        orm_mode = True


class IndicatorSetSchema(BaseModel):
    Id: Optional[int] = None
    Name: str
    Description: str
    MeasurementFrequency: str
    UnitMeasure: str
    ObjectiveId: int
    MetricTypeId: int

    class Config:
        orm_mode = True


class MetricTypeSetSchema(BaseModel):
    Id: Optional[int] = None

    class Config:
        orm_mode = True


class DataIndicatorSetSchema(BaseModel):
    Id: Optional[int] = None
    Value: float
    Date: datetime
    IndicatorId: int

    class Config:
        orm_mode = True


class TargetSetSchema(BaseModel):
    Id: Optional[int] = None
    Description: str
    ExpectedValue: float
    DeadlineDate: datetime
    IndicatorId: int

    class Config:
        orm_mode = True
