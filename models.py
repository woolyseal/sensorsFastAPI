from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class SensorType(Base):
    __tablename__ = "sensor_type"

    id = Column(BigInteger, primary_key=True)
    sensor_name = Column(String)
    sensor_manufacturer = Column(String)

    # Relationship to the Sensor table
    sensors = relationship("Sensor", back_populates="sensor_type")

class Location(Base):
    __tablename__ = "sensor_location"

    id = Column(BigInteger, primary_key=True)
    indoor = Column(Boolean)
    altitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    country = Column(String, index=True)

    # Relationship to the Sensor table
    sensors = relationship("Sensor", back_populates="location")


class Sensor(Base):
    __tablename__ = "weather_sensor"
    
    id = Column(BigInteger, primary_key=True, index=True)
    sensor_type = relationship("SensorType", back_populates="sensortype")
    sensor_pin = Column(String)
    sensor_type_id = Column(BigInteger, ForeignKey('sensor_type.id'))
    location_id = Column(BigInteger, ForeignKey('sensor_location.id'))

    # Relationship to SensorType
    sensor_type = relationship("SensorType", back_populates="sensors")

    # Relationship to Location
    location = relationship("Location", back_populates="sensors")

    # Relationship to the SensorData table
    sensordata = relationship("SensorData", back_populates="sensordata")


class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(BigInteger, primary_key=True)
    value = Column(Float)
    value_type = Column(String, index=True)
    measurement = Column(DateTime, server_default=func.now())
    sensor_id = Column(BigInteger, ForeignKey('weather_sensor.id'))

    # Relationship to Location
    sensordata = relationship("Sensor", back_populates="sensordata")
