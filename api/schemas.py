from pydantic import BaseModel

class DetectionDataSchema(BaseModel):
    image_path: str
    box_coordinates: str
    confidence_score: float
    class_label: str

class DetectionDataCreate(DetectionDataSchema):
    pass

class MedicalDataSchema(BaseModel):
    message_id: str
    sender_id: str
    message_text: str
    channel: str

class MedicalDataCreate(MedicalDataSchema):
    pass