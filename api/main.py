from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api import crud, models, schemas  # Ensure correct import path
from api.database import SessionLocal, engine  # Ensure correct import path

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/detection_data/", response_model=schemas.DetectionDataSchema)
def create_detection_data(detection_data: schemas.DetectionDataCreate, db: Session = Depends(get_db)):
    return crud.create_detection_data(db, detection_data)

@app.post("/medical_data/", response_model=schemas.MedicalDataSchema)
def create_medical_data(medical_data: schemas.MedicalDataCreate, db: Session = Depends(get_db)):
    return crud.create_medical_data(db, medical_data)

@app.get("/detection_data/", response_model=list[schemas.DetectionDataSchema])
def read_detection_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    detection_data = crud.get_detection_data(db, skip=skip, limit=limit)
    return detection_data

@app.get("/medical_data/", response_model=list[schemas.MedicalDataSchema])
def read_medical_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    medical_data = crud.get_medical_data(db, skip=skip, limit=limit)
    return medical_data