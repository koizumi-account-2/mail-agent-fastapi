from pydantic import BaseModel
from typing import List

class PastEvent(BaseModel):
    recurring_events_str: str
    single_events_str: str


class BusySlot(BaseModel):
    day: str    
    time_range: str

class FrequentSlot(BaseModel):
    time_range: str

class EventTrend(BaseModel):
    busy_slots: List[BusySlot]
    frequent_slots: List[FrequentSlot]
    title_patterns: List[str]
