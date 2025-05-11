from fastapi import APIRouter, Depends
from chains.calendar.get_event_trend_chain.past_event_trend_agent import PastEventTrendAgent
from util.common import get_access_token
from modules.config import model
from features.calendar.services.imp.google_calendar_service import GoogleCalendarService
from pydantic import BaseModel
from chains.calendar.models import EventTrend
from datetime import datetime,timedelta,timezone
import math
from typing import List
from features.calendar.services.common_calendar_service import CandidateDay,get_candidate_days
from features.calendar.models import CalenderEventFilterParams
from features.calendar.schemas.calendar_schema import InsertEventDTO


calendar_router = APIRouter()
class AvailableSlotsRequest(BaseModel):
    insert_event:InsertEventDTO
    trend:EventTrend        
    travel_time_seconds:int

@calendar_router.get("/")
async def get_all_events(offset_days:int=2,duration_days:int=30,access_token: str = Depends(get_access_token)):
    """
    今後のイベントを取得する
    """
    google_calendar_service = GoogleCalendarService(access_token)
    params = CalenderEventFilterParams(
        start_date=datetime.now(timezone.utc) + timedelta(days=offset_days),
        duration=duration_days
    )
    result = await google_calendar_service.get_calendar_events(params)
    return result

@calendar_router.get("/past")
async def get_past_events(access_token: str = Depends(get_access_token)):
    """
    過去のイベントを取得する
    """
    past_event_trend_agent = PastEventTrendAgent(model,access_token)
    result = await past_event_trend_agent.get_chain().ainvoke({})
    return result


@calendar_router.get("/available")
async def get_available_slots(insert_event:InsertEventDTO,offset_days:int=2,duration_days:int=7,access_token: str = Depends(get_access_token)):
    """
    空いている時間を取得する
    """
    google_calendar_service = GoogleCalendarService(access_token)
    result = await google_calendar_service.get_insert_event_candidates(insert_event,offset_days,duration_days)
    return result

@calendar_router.post("/candidates")
async def get_available_slots(request:AvailableSlotsRequest,max_candidates_per_day:int=3,offset_days:int=2,duration_days:int=7,access_token: str = Depends(get_access_token)):
    """
    候補日を取得する
    """
    print("duration_days",duration_days)
    trend = request.trend
    travel_time_minutes = get_duration(request.travel_time_seconds)
    request.insert_event.duration = travel_time_minutes*2 + request.insert_event.duration
    google_calendar_service = GoogleCalendarService(access_token)
    result:List[CandidateDay]  = await google_calendar_service.get_insert_event_candidates(request.insert_event,offset_days,duration_days)
    print("CandidateDay",len(result))
    candidate_days,candidate_days_all = get_candidate_days(trend,result,max_candidates_per_day)
    print("candidate_days",len(candidate_days))
    print("candidate_days_all",len(candidate_days_all))
    return {
        "candidate_days":candidate_days,
        "candidate_days_all":candidate_days_all
    }


# 移動時間を30分単位で切り上げて、0.5時間単位に変換する
def get_duration(travel_time_seconds:int,block_size_minutes:int=30):
    blocks = math.ceil(travel_time_seconds / (block_size_minutes * 60)) + 1 # 30分単位のブロック数
    return blocks * block_size_minutes  # 分に変換   