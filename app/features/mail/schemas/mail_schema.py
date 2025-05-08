from typing import List, Optional
from pydantic import BaseModel

class MailMessageDTO(BaseModel):
    id: str
    snippet: str
    subject: str
    sender: str
    date: str
    content: str

class ThreadDTO(BaseModel):
    threadId: str
    messages: List[MailMessageDTO]


class ThreadListResponse(BaseModel):
    threadIds: List[str]
    nextPageToken: Optional[str] = None