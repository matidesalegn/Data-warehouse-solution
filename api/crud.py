# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# CRUD operations for DetectionData
def get_detection_datas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DetectionData).offset(skip).limit(limit).all()

def create_detection_data(db: Session, detection_data: schemas.DetectionDataCreate):
    db_detection_data = models.DetectionData(**detection_data.dict())
    db.add(db_detection_data)
    db.commit()
    db.refresh(db_detection_data)
    return db_detection_data

# CRUD operations for MedicalData
def get_medical_datas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MedicalData).offset(skip).limit(limit).all()

def create_medical_data(db: Session, medical_data: schemas.MedicalDataCreate):
    db_medical_data = models.MedicalData(**medical_data.dict())
    db.add(db_medical_data)
    db.commit()
    db.refresh(db_medical_data)
    return db_medical_data