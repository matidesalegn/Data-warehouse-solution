# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class DetectionDataBase(BaseModel):
    image_path: str
    box_coordinates: str
    confidence_score: float
    class_label: str

class DetectionDataCreate(DetectionDataBase):
    pass

class DetectionData(DetectionDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode: True

class MedicalDataBase(BaseModel):
    sender_id: str
    message_text: str
    channel: str

class MedicalDataCreate(MedicalDataBase):
    pass

class MedicalData(MedicalDataBase):
    message_id: UUID

    class Config:
        orm_mode: True