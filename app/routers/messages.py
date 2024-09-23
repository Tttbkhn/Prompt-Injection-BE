from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import List, Annotated
from users import current_active_user
from models.messages import Message, NewMessage
from models.conversations import Conversation
from beanie import PydanticObjectId
from db import User

router = APIRouter(prefix="/messages",
                   tags=["messages"], dependencies=[Depends(current_active_user)])


@router.post("/new_message", response_description={"Post a message in an empty conversation, a new conversation will be created"})
async def post_new_message(message: NewMessage, user: User = Depends(current_active_user)) -> Message:
    new_conversation = Conversation(name="New conversation", user_id=user.id)
    await new_conversation.create()
    message = Message(conversation_id=new_conversation.id, text=message.text)
    await message.create()
    return message


@router.get("/{conversation_id}", response_description={"Get all messages by conversation id"})
async def get_messages(conversation_id: PydanticObjectId) -> List[Message]:
    messages = await Message.find(Message.conversation_id == conversation_id).to_list()
    return messages


@router.post("/{conversation_id}", response_description={"Post a message in a conversation"})
async def post_message(conversation_id: PydanticObjectId, message: NewMessage) -> Message:
    conversation = await Conversation.get(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Conversation with id {conversation_id} not found"
        )
    message = Message(conversation_id=conversation_id, text=message.text)
    await message.create()
    return message
