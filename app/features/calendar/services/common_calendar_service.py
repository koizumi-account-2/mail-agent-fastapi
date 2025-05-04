from features.calendar.services.calendar_service import CalendarService
from features.calendar.models import CalenderEventFilterParams
from features.calendar.schemas.calendar_schema import CalendarEventDTO,InsertEventDTO
from typing import List,Tuple
from datetime import datetime,timedelta,time
import jpholiday

#　テストが必要

start_hour = 9
end_hour = 18
slot_minutes = 30

lunch_start_hour = 12
lunch_end_hour = 13

from zoneinfo import ZoneInfo
tz = ZoneInfo("Asia/Tokyo")

def find_candidate_slots(start_date:datetime,insert_event:InsertEventDTO, existing_events:List[CalendarEventDTO], slot_minutes=30, start_hour=9, end_hour=18):
    candidate_slots = []
    tz = ZoneInfo("Asia/Tokyo")

    end_date = start_date + timedelta(days=7)
    required_slots = insert_event.duration // slot_minutes  # e.g. 120 / 30 = 4

    for n in range((end_date.date() - start_date.date()).days + 1):
        current_date = start_date.date() + timedelta(days=n)

        if current_date.weekday() < 5 and not jpholiday.is_holiday(current_date):  # 平日かつ祝日でない
            for hour in range(start_hour, end_hour):
                if hour >= lunch_start_hour and hour <= lunch_end_hour:
                    continue
                for minute in (0, 30):
                    start_time = datetime.combine(current_date, time(hour, minute, tzinfo=tz))
                    end_time = start_time + timedelta(minutes=slot_minutes * required_slots)

                    if end_time.time() <= time(end_hour, 0):
                        if is_slot_available((start_time, end_time), existing_events):
                            candidate_slots.append((start_time, end_time))

    return candidate_slots
            
            
def is_slot_available(candidate_slot, existing_events):
    c_start, c_end = candidate_slot
    for existing_event in existing_events:
        if existing_event.start.dateTime is None and existing_event.start.date is not None:
            print("終日イベント",existing_event.start.date)
            target_date = datetime.strptime(existing_event.start.date, "%Y-%m-%d")
            e_start = datetime.combine(target_date, time(start_hour, 0, tzinfo=tz))
            e_end = datetime.combine(target_date, time(end_hour, 0, tzinfo=tz))
        else:   
            e_start = existing_event.start.dateTime
            e_end = existing_event.end.dateTime

        # 重なっているか？（→ NG）
        if c_start < e_end and c_end > e_start:
            print(f"[NG] Conflict with: {e_start} ~ {e_end}")
            return False

    # 全イベントと重ならなければOK
    return True