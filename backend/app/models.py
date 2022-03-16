from pydantic import EmailStr, BaseModel, Field
from typing import Dict

class EmailSchema(BaseModel):
    email: EmailStr = Field(...)
    subject: str = Field(...)
    body: Dict[str, str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "maxwellwachira67@gmail.com", 
                "subject": "FastAPI is Awesome!!",
                "body": {
                    "title": "FastAPI MAILER",
                    "message": "This email is sent by FastAPI"
                }
            }
        }
