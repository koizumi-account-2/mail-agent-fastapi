from abc import ABC, abstractmethod
from typing import List, Dict
from features.calendar.schemas.calendar_schema import CalendarEventListResponse,CalendarEventDTO,InsertEventDTO
from features.calendar.models import CalenderEventFilterParams
class CalendarService(ABC):

    @abstractmethod
    async def get_calendar_list(self):
        ...

    @abstractmethod 
    async def get_calendar_events(self,params:CalenderEventFilterParams)->CalendarEventListResponse:
        ...

    @abstractmethod
    async def get_calendar_event_by_id(self,event_id:str)->CalendarEventDTO:
        ...

    @abstractmethod
    async def get_insert_event_candidates(self,event:InsertEventDTO,offset_days:int=2,duration_days:int=7):
        ...




# {
#   "busy_slots": [
#     { "day": "金曜日", "time_range": "10:00-11:00" },
#     { "day": "水曜日", "time_range": "15:00-16:00" }
#   ],
#   "frequent_slots": [
#     { "day": "火曜日", "time_range": "13:00-14:00" },
#     { "day": "木曜日", "time_range": "09:00-10:00" },
#     { "day": "月曜日", "time_range": "16:00-17:00" }
#   ],
#   "title_patterns": [
#     "[PJ名] 定例",
#     "営業週次",
#     "社内レビュー",
#     "1on1",
#     "議事録付き会議"
#   ]
# }