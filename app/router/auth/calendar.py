from fastapi import APIRouter, Depends
from chains.calendar.get_event_trend_chain.past_event_trend_agent import PastEventTrendAgent
from util.common import get_access_token
from modules.config import model
from features.calendar.services.imp.google_calendar_service import GoogleCalendarService
from pydantic import BaseModel
from datetime import datetime

from features.calendar.schemas.calendar_schema import InsertEventDTO


calendar_router = APIRouter()



@calendar_router.get("/past")
async def get_past_events(access_token: str = Depends(get_access_token)):

    print("access_token",access_token)
    past_event_trend_agent = PastEventTrendAgent(model,access_token)
    result = await past_event_trend_agent.get_chain().ainvoke("株式会社テスト")
    return result


@calendar_router.get("/available")
async def get_available_slots(insert_event:InsertEventDTO,access_token: str = Depends(get_access_token)):
    google_calendar_service = GoogleCalendarService(access_token)
    result = await google_calendar_service.get_insert_event_candidates(insert_event)
    return result