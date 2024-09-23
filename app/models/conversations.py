from datetime import datetime
from typing import Optional
from beanie import Document
from beanie import PydanticObjectId


class Conversation(Document):
    name: str
    user_id: PydanticObjectId
    time: Optional[datetime] = datetime.now()

    class Settings:
        name = "Conversation"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "How to make an REST API",
                "user_id": "5eb7cf5a86d9755df3a6c593",
                "time": datetime.now()
            }
        }


class NewConversation(Document):
    name: str

    class Settings:
        name = "Conversation"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "How to make an REST API",
            }
        }
