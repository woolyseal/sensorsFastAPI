from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError

import requests
import crud, models, schemas
from datetime import datetime
import pytz


models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI(
    title="Weatherdata",
    description="Using FastAPI to save and display weatherdata",
    version="0.1"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@app.get('/sensor/{id}', response_model=schemas.Sensor, status_code=200)
def get_sensor(id: str, db: Session = Depends(get_db)) -> models.Sensor:
    db_sensor = crud.get_sensor(db, id=id)
    if db_sensor is None:
        raise HTTPException(
            status_code=404, detail=f"No sensor {id} found."
        )

    return db_sensor

@app.get('/sensor_type/{id}', response_model=schemas.SensorType, status_code=200)
def get_sensor_type(id: str, db: Session = Depends(get_db)) -> models.SensorType:
    db_sensor_type = crud.get_sensor_type(db, id=id)
    if db_sensor_type is None:
        raise HTTPException(
            status_code=404, detail=f"No sensor_type {id} found."
        )

    return db_sensor_type

# Fetch data from an external API
@app.get("/import-sensors/")
async def import_sensors(db: Session = Depends(get_db)):
    try:
        # URL of the external API
        api_url = "https://data.sensor.community/static/v1/data.json"
        
        # Fetch JSON data from the external API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        
        sensors_data = response.json()  # The data should be a list of sensor records
        
        # Iterate over the JSON data and create Sensor objects
        for sensor_data in sensors_data:
            if "sensor" in sensor_data:
                sensor_info = sensor_data.get("sensor")
                location = sensor_data.get("location")
                format_string = "%Y-%m-%d %H:%M:%S"
                
                # Localize to UTC (or any other timezone)
                timezone = pytz.utc  # For UTC
                timestamp_utc = timezone.localize(datetime.strptime(sensor_data["timestamp"], format_string))

                # Searching for existing information
                sensor_type = db.query(models.SensorType).filter(models.SensorType.id == sensor_info["sensor_type"]["id"]).first()
                sensor_location = db.query(models.Location).filter(models.Location.id == location["id"]).first()
                sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_info["id"]).first()

                if not sensor_type:
                    sensor_type = models.SensorType(
                        id=sensor_info["sensor_type"]["id"],
                        sensor_name=sensor_info["sensor_type"]["name"],
                        sensor_manufacturer=sensor_info["sensor_type"]["manufacturer"]
                    )
                try:
                    db.add(sensor_type)
                    db.commit()
                    db.refresh(sensor_type)
                except Exception as e:
                    breakpoint()

                if not sensor_location:
                    sensor_location = models.Location(
                        id=location["id"],
                        indoor=True if location["indoor"]==1 else False,
                        altitude=location["altitude"] if location["altitude"] else 0.0,
                        latitude=location["latitude"] if location["latitude"] else 0.0,
                        longitude=location["longitude"] if location["longitude"] else 0.0,
                        country=location["country"]
                    )
                try:
                    db.add(sensor_location)
                    db.commit()
                    db.refresh(sensor_location)
                except Exception as e:
                    breakpoint()

                if not sensor:
                    sensor = models.Sensor(
                        id=sensor_info["id"],
                        sensor_pin=sensor_info["pin"],
                        sensor_type_id=sensor_type.id,
                        location_id=sensor_location.id,
                    )
                try:
                    db.add(sensor)
                    db.commit()
                    db.refresh(sensor)
                except Exception as e:
                    breakpoint()

                for val in sensor_data.get("sensordatavalues"):
                    try:
                        sensorvalue = db.query(models.SensorData).filter(models.SensorData.id == val["id"]).first()
                    except KeyError:
                        sensorvalue = None
                        print(val)
                    if not sensorvalue:
                        try:
                            sensorvalue = models.SensorData(
                                id=val["id"],
                                value=float(val["value"]),
                                value_type=val["value_type"],
                                measurement=timestamp_utc,
                                sensor_id=sensor.id
                            )
                        except ValueError:
                            print(val)
                    try:
                        db.add(sensorvalue)
                        db.commit()
                        db.refresh(sensorvalue)
                    except Exception as e:
                        breakpoint()

        return {"message": "Data imported successfully"}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data from API: {e}")
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session in case of error
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
