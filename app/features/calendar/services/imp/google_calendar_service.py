from features.calendar.services.calendar_service import CalendarService
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from modules.log import log_async
from features.calendar.schemas.calendar_schema import CalendarEventListResponse,CalendarEventDTO,InsertEventDTO,EventTime
from features.calendar.models import CalenderEventFilterParams
from features.calendar.services.common_calendar_service import find_candidate_slots
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
    async def get_calendar_events(self,params:CalenderEventFilterParams)->CalendarEventListResponse:
        """
        カレンダーの全てのイベントを取得する
        """
        duration = params.duration
        start_date = params.start_date.isoformat()

        time_max = (params.start_date + timedelta(days=duration)).isoformat()
        query_params = {
            "calendarId": "primary",
            "maxResults": 100,
            "timeMin": start_date,
            "timeMax": time_max,
        }
        results = self.service.events().list(**query_params).execute()
        print("results",results)
        return CalendarEventListResponse(events=[google_calendar_event_to_calendar_event_dto(event) for event in results.get("items", [])])

    @log_async
    async def get_calendar_event_by_id(self,event_id:str)->CalendarEventDTO:
        """
        カレンダーのイベントを取得する
        """
        return google_calendar_event_to_calendar_event_dto(self.service.events().get(eventId=event_id).execute())    

    @log_async
    async def get_insert_event_candidates(self,event:InsertEventDTO):
        """
        カレンダーのイベントを挿入する候補の時間を取得する
        """
        candidate_slots = []
        start_date = datetime.now(timezone.utc) + timedelta(days=2)
        
        for participant in event.participants:
            # 既存のイベントを取得する
            existing_event = await self.get_calendar_events(CalenderEventFilterParams(start_date=start_date,duration=7))
            print("existing_eventの件数：",existing_event.events)
            # 候補の時間を取得する
            candidate_slots.extend(find_candidate_slots(start_date,event,existing_event.events))
        # 複数人の場合はここで調整が必要
        return candidate_slots

def google_calendar_event_to_calendar_event_dto(event_dict):
    return CalendarEventDTO(
        id=event_dict["id"],
        status=event_dict["status"],
        summary=event_dict.get("summary", ""),
        start=EventTime(**event_dict["start"]),
        end=EventTime(**event_dict["end"]),
        recurrence=event_dict.get("recurrence"),
    )


    # @log_async
    # async def get_past_calendar_events(self)->CalendarEventListResponse:
    #     """
    #     過去のカレンダーのイベントを取得する
    #     """
    #     today = datetime.now(timezone.utc)
    #     time_min = (today - timedelta(days=30)).isoformat()
    #     time_max = today.isoformat()
    #     query_params = {
    #         "calendarId": "primary",
    #         "maxResults": 100,
    #         "timeMin": time_min,
    #         "timeMax": time_max,
    #     }   
    #     events = self.service.events().list(**query_params).execute().get("items", [])

    #     return CalendarEventListResponse(events=[CalendarEventDTO(**event) for event in events])