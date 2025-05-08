from pydantic import BaseModel,field_validator
from typing import List, Optional,Union
from datetime import datetime
from zoneinfo import ZoneInfo
class EventTime(BaseModel):
    dateTime: Optional[datetime] = None
    date: Optional[str] = None
    timeZone: Optional[str] = None


class CalendarEventDTO(BaseModel):
    id: str
    status: str
    summary: str
    start: EventTime
    end: EventTime
    recurrence: Optional[List[str]] = None


class InsertEventDTO(BaseModel):
    duration: int
    summary: str
    participants: List[str] 
    
class CalendarEventListResponse(BaseModel):
    events: List[CalendarEventDTO]