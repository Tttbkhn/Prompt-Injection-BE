from fastapi import APIRouter, Depends
from typing import List
from models.conversations import Conversation, NewConversation
from users import current_active_user, User

router = APIRouter(prefix="/conversations",
                   tags=["conversations"], dependencies=[Depends(current_active_user)])


@router.get("/")
async def get_conversations(user: User = Depends(current_active_user)) -> List[Conversation]:
    conversations = await Conversation.find(Conversation.user_id == user.id).to_list()
    return conversations


@router.post("/", response_description="Create new conversation")
async def create_conversation(conversation: NewConversation, user: User = Depends(current_active_user)) -> Conversation:
    new_conversation = Conversation(name=conversation.name, user_id=user.id)
    await new_conversation.create()
    return new_conversation
