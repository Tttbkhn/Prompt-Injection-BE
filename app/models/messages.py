from datetime import datetime

from beanie import Document, PydanticObjectId
from models.conversations import Conversation
from typing import Optional


class Message(Document):
    is_bot: Optional[bool] = False
    text: str
    conversation_id: PydanticObjectId
    time: Optional[datetime] = datetime.now()

    class Settings:
        name = "Message"

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello Chatbox, how many colors does the rainbow have?",
                "conversation_id": "5eb7cf5a86d9755df3a6c593",
                "time": datetime.now(),
                "is_bot": False
            }
        }


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
