import math 
import asyncio
from features.calendar.services.imp.google_calendar_service import GoogleCalendarService
from features.calendar.schemas.calendar_schema import InsertEventDTO

async def get_candidate_chain(inputs):
    travel_time_seconds = inputs["travel_time"].duration
    duration = get_duration(travel_time_seconds) * 2 + 60

    google_calendar_service = GoogleCalendarService(access_token)
    insert_event = InsertEventDTO(
        duration=duration,
        summary=inputs["info"].company_name,
        participants=["test@example.com"]
    )
    candidate_slots = await google_calendar_service.get_insert_event_candidates(insert_event)
    print(candidate_slots)

# 移動時間を30分単位で切り上げて、0.5時間単位に変換する
def get_duration(travel_time_seconds:int,block_size_minutes:int=30):
    blocks = math.ceil(travel_time_seconds / (block_size_minutes * 60))  # 30分単位のブロック数
    return blocks * block_size_minutes  # 分に変換