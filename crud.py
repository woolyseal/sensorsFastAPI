from models import Sensor, SensorData, SensorType, Location
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_sensor(db: Session, id: str):
    return db.query(Sensor).filter(Sensor.id == id).first()

def get_sensor_type(db: Session, id: str):
    return db.query(SensorType).filter(SensorType.id == id).first()

def get_sensors(db: Session):
    return db.query(Sensor).all()[:10]

def get_sensor_types(db: Session):
    return db.query(SensorType).all()[:10]

def get_sensor_data_with_sensor_info(db: Session, id: int):
    # Query to join Sensor and SensorData based on sensor_id
    stmt = (
        select(Sensor.id, Sensor.sensor_pin, SensorData.id, SensorData.measurement, SensorData.value, SensorData.value_type)
        .join(SensorData, Sensor.id == SensorData.sensor_id)  # Joining Sensor with SensorData
        .filter(Sensor.id == id)  # Filter by the specific sensor_id
    )
    
    # Execute the query
    result = db.execute(stmt).fetchall()
    
    return result