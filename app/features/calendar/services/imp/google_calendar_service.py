from features.calendar.services.calendar_service import CalendarService
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from modules.log import log_async
from features.calendar.schemas.calendar_schema import CalendarEventListResponse,CalendarEventDTO    
class GoogleCalendarService(CalendarService):
    def __init__(self, access_token: str):
        credentials = Credentials(
            token=access_token,
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        self.service = build("calendar", "v3", credentials=credentials) 

    @log_async
    async def get_calendar_list(self):
        """
        カレンダーのリストを取得する
        """
        return self.service.calendarList().list().execute()

    @log_async
    async def get_all_calendar_events(self,params:dict)->CalendarEventListResponse:
        """
        カレンダーの全てのイベントを取得する
        """
        duration = params.get("duration", 21)
        today = datetime.now(timezone.utc).isoformat() + 'Z'
        # 少なくとも２日後から取得する
        time_min = today + timedelta(days=2)
        time_max = time_min + timedelta(days=duration)
        query_params = {
            "userId": "primary",
            "maxResults": 100,
            "timeMin": time_min,
            "timeMax": time_max,
        }
        results = self.service.events().list(**query_params).execute()
        return CalendarEventListResponse(events=[CalendarEventDTO(**event) for event in results.get("items", [])])

    @log_async
    async def get_calendar_event_by_id(self,event_id:str)->CalendarEventDTO:
        """
        カレンダーのイベントを取得する
        """
        return CalendarEventDTO(**self.service.events().get(eventId=event_id).execute())    

    @log_async
    async def get_past_calendar_events(self)->CalendarEventListResponse:
        """
        過去のカレンダーのイベントを取得する
        """
        today = datetime.now(timezone.utc)
        time_min = (today - timedelta(days=30)).isoformat()
        time_max = today.isoformat()
        query_params = {
            "calendarId": "primary",
            "maxResults": 100,
            "timeMin": time_min,
            "timeMax": time_max,
        }   
        events = self.service.events().list(**query_params).execute().get("items", [])

        return CalendarEventListResponse(events=[CalendarEventDTO(**event) for event in events])