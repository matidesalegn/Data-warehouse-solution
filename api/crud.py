from sqlalchemy.orm import Session
from models import DetectionData, MedicalData
from schemas import DetectionDataCreate, MedicalDataCreate
from database import SessionLocal

def create_detection_data(db: Session, detection_data: DetectionDataCreate):
    db_detection_data = DetectionData(**detection_data.dict())
    db.add(db_detection_data)
    db.commit()
    db.refresh(db_detection_data)
    return db_detection_data

def create_medical_data(db: Session, medical_data: MedicalDataCreate):
    db_medical_data = MedicalData(**medical_data.dict())
    db.add(db_medical_data)
    db.commit()
    db.refresh(db_medical_data)

def get_detection_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetectionData).offset(skip).limit(limit).all()

def get_medical_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MedicalData).offset(skip).limit(limit).all()