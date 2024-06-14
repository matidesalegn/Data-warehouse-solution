from sqlalchemy import Column, Integer, Text, Float, TIMESTAMP
from database import Base

class DetectionData(Base):
    __tablename__ = "detection_datas"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(Text)
    box_coordinates = Column(Text)
    confidence_score = Column(Float)
    class_label = Column(Text)
    timestamp = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

class MedicalData(Base):
    __tablename__ = "medical_datas"

    message_id = Column(Text, primary_key=True, index=True)
    sender_id = Column(Text)
    message_text = Column(Text)
    channel = Column(Text)