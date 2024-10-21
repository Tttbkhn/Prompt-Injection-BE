from fastapi import APIRouter, Depends
from typing import List
from models.conversations import Conversation, NewConversation
from models.messages import Message
from users import current_active_user, User
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v2/conversations",
                   tags=["conversations"], dependencies=[Depends(current_active_user)])


@router.get("/")
async def get_conversations(user: User = Depends(current_active_user)) -> List[Conversation]:
    conversations = await Conversation.find(Conversation.user_id == user.id).to_list()
    return conversations

@router.delete("/{conversation_id}")
async def delete_conversations(conversation_id: PydanticObjectId) -> Conversation:
    conversation = await Conversation.find_one(Conversation.id == conversation_id)
    if conversation:
        await conversation.delete()
    await Message.find(Message.conversation_id == conversation_id).delete()
    return conversation


@router.post("/", response_description="Create new conversation")
async def create_conversation(conversation: NewConversation, user: User = Depends(current_active_user)) -> Conversation:
    new_conversation = Conversation(name=conversation.name, user_id=user.id)
    await new_conversation.create()
    return new_conversation
