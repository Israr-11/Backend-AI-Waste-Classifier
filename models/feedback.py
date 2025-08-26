from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class UserFeedBack(BaseModel):
    image_hash: str = Field(..., description="Hash of the image")
    is_correct: bool = Field(..., description="Checking if the classification is correct")
    correct_category: str = Field(default='Same as above', description="Correct category of the image")
    tried_techniques: Optional[List[str]] = Field(default=None, description="Techniques the user has tried")
    entryTime: datetime = Field(default=datetime.now(), description="Time the feedback was given")

    @field_validator('entryTime', mode="before")
    def validate_entry_time(cls, v):
        if isinstance(v, str):  # CONVERTING STRING TIMESTAMPS TO DATETIME
            return datetime.fromisoformat(v)
        if not isinstance(v, datetime):
            raise ValueError('entryTime must be a datetime object')
        return v

    def to_dict(self):
        return self.model_dump()  # CONVERTING TO DICTIONARY FOR MONGODB
