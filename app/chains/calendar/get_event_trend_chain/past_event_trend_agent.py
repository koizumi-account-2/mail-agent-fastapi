from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from chains.calendar.models import EventTrend,PastEvent
from features.calendar.services.imp.google_calendar_service import GoogleCalendarService
from features.calendar.schemas.calendar_schema import CalendarEventListResponse,CalendarEventDTO
from chains.calendar.get_event_trend_chain.prompt import weekly_meeting_analysis_prompt
from typing import List


class PastEventTrendAgent:   
    def __init__(self, llm: ChatOpenAI, access_token:str):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=EventTrend)
        self.access_token = access_token
        self.chain = self._build_chain()

    async def get_psat_events_chain(self,input)->dict:
        """
        過去のイベントを取得する    
        Tuple[繰り返しイベントの文字列,単発イベントの文字列] で返す 
        """
        calendar_service = GoogleCalendarService(self.access_token)
        response:CalendarEventListResponse = await calendar_service.get_past_calendar_events()

        print("response",event_to_string(response.events))
        return event_to_string(response.events)

    def _build_chain(self) -> Runnable:
        return (
            self.get_psat_events_chain
            | weekly_meeting_analysis_prompt
            | self.llm
            | self.parser
        )
    def get_chain(self) -> Runnable:
        return self.chain



def event_to_string(events:List[CalendarEventDTO])->dict:
    recurring_events = []
    single_events = []
    for event in events:
        # 繰り返しイベント
        if( event.recurrence and len(event.recurrence) > 0):
            recurring_events.append(event)
        # 単発イベント
        else: 
            single_events.append(event)

    recurring_events_str = "\n".join([
        f"イベント名：{event.summary}\n"
        f"開始日時：{event.start.dateTime}\n"
        f"終了日時：{event.end.dateTime}\n"
        f"繰り返しのルール：{','.join(event.recurrence)}\n"
        for event in recurring_events
    ])
    single_events_str = "\n".join([
        f"イベント名：{event.summary}\n"
        f"開始日時：{event.start.dateTime}\n"
        f"終了日時：{event.end.dateTime}\n"
        for event in single_events
    ])
    return {
        "recurring_events":recurring_events_str,
        "single_events":single_events_str
    }