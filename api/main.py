# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoints for DetectionData
@app.post("/detection_datas/", response_model=schemas.DetectionData)
def create_detection_data(detection_data: schemas.DetectionDataCreate, db: Session = Depends(get_db)):
    return crud.create_detection_data(db=db, detection_data=detection_data)

@app.get("/detection_datas/", response_model=List[schemas.DetectionData])
def read_detection_datas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    detection_datas = crud.get_detection_datas(db, skip=skip, limit=limit)
    return detection_datas

# Endpoints for MedicalData
@app.post("/medical_datas/", response_model=schemas.MedicalData)
def create_medical_data(medical_data: schemas.MedicalDataCreate, db: Session = Depends(get_db)):
    return crud.create_medical_data(db=db, medical_data=medical_data)

@app.get("/medical_datas/", response_model=List[schemas.MedicalData])
def read_medical_datas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    medical_datas = crud.get_medical_datas(db, skip=skip, limit=limit)
    return medical_datas