from pydantic import BaseModel
from typing import List, Optional

class EventTime(BaseModel):
    dateTime: str
    timeZone: str

class CalendarEventDTO(BaseModel):
    id: str
    status: str
    summary: str
    start: EventTime
    end: EventTime
    recurrence: Optional[List[str]] = None


    
class CalendarEventListResponse(BaseModel):
    events: List[CalendarEventDTO]