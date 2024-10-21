from datetime import datetime

from beanie import Document, PydanticObjectId
from typing import Optional

class NewMessage(Document):
    text: str

    class Settings:
        name = "Message"

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello Chatbox, how many colors does the rainbow have?",
            }
        }
