from fastapi import APIRouter, Depends
from chains.calendar.get_event_trend_chain.past_event_trend_agent import PastEventTrendAgent
from util.common import get_access_token
from modules.config import model

calendar_router = APIRouter()

@calendar_router.get("/past")
async def get_past_events(access_token: str = Depends(get_access_token)):

    print("access_token",access_token)
    past_event_trend_agent = PastEventTrendAgent(model,access_token)
    result = await past_event_trend_agent.get_chain().ainvoke("株式会社テスト")
    return result

