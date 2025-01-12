from sqlalchemy.orm import Session

import models, schemas

def get_sensor(db: Session, id: str):
    return db.query(models.Sensor).filter(models.Sensor.id == id).first()

def get_sensor_type(db: Session, id: str):
    return db.query(models.SensorType).filter(models.SensorType.id == id).first()

def get_sensors(db: Session):
    return db.query(models.Sensor).all()

def get_sensor_types(db: Session):
    return db.query(models.SensorType).all()
