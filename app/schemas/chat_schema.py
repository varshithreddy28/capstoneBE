from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    content: str
    timestamp: datetime
    sender: str

class ChatSessionCreate(BaseModel):
    content: str
    timestamp: datetime

class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    messages: List[Message]
    createdAt: datetime
