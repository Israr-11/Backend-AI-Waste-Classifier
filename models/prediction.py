from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class ImageProcessingAndPrediction(BaseModel):
    image_hash: str = Field(..., description="Hash of the image")
    original_prediction: str = Field(..., description="Original prediction of the image")
    correct_prediction: str = Field(..., description="Classification of the image")
    # confidence: float = Field(..., description="Confidence of the prediction")
    category: str = Field(..., description="Category of the image")
    entryTime: datetime = Field(default=datetime.now(), description="Time the image was uploaded")

    @field_validator('entryTime', mode="before")
    def validate_entry_time(cls, v):
        if isinstance(v, str):  # ENSURING STRING TIMESTAMPS CONVERT TO DATETIME
            return datetime.fromisoformat(v)
        if not isinstance(v, datetime):
            raise ValueError('entryTime must be a datetime object')
        return v

    def to_dict(self):
        return self.model_dump()  # CONVERTING TO DICTIONARY FOR MONGODB
