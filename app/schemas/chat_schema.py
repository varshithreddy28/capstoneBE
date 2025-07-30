from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class Message(BaseModel):
    content: str
    timestamp: datetime
    sender: str

class ChatSessionCreate(BaseModel):
    content: str
    timestamp: datetime

class ChatSessionResponse(BaseModel):
    content: str
    sender: Literal["Assistant"]
    timestamp: datetime

class ChatMessageResponse(BaseModel):
    message: str
    timestamp: datetime
