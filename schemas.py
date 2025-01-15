from pydantic import BaseModel
from datetime import datetime


class Sensor(BaseModel):
    id: int
    sensor_pin: str
    sensor_type_id: int
    location_id: int
    
    class Config:
        from_attributes = True


class SensorType(BaseModel):
    id: int
    sensor_name: str
    sensor_manufacturer: str
    
    class Config:
        from_attributes = True


class Location(BaseModel):
    id: int
    indoor: bool = False
    altitude: float
    latitude: float
    longitude: float
    country: str
    
    class Config:
        from_attributes = True


class SensorData(BaseModel):
    id: int
    value: float
    value_type: str
    measurement: datetime | None
    sensor_id: int
    
    class Config:
        from_attributes = True


class SensorDataResponse(BaseModel):
    id: int
    sensor_pin: str
    sensor_data_id: int
    measurement: datetime
    value: float
    value_type: str

    class Config:
        from_attributes = True