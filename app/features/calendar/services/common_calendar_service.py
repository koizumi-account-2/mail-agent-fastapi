from features.calendar.services.calendar_service import CalendarService
from features.calendar.models import CalenderEventFilterParams,CandidateDay,Slot
from features.calendar.schemas.calendar_schema import CalendarEventDTO,InsertEventDTO
from typing import List,Tuple
from chains.calendar.models import EventTrend
from datetime import datetime,timedelta,time
import jpholiday
import math
#　テストが必要

start_hour = 9
end_hour = 18
slot_minutes = 30

lunch_start_hour = 12
lunch_end_hour = 13

from zoneinfo import ZoneInfo
tz = ZoneInfo("Asia/Tokyo")

def find_candidate_slots(start_date:datetime,insert_event:InsertEventDTO, existing_events:List[CalendarEventDTO], slot_minutes=30, start_hour=9, end_hour=18, duration_days:int=7) -> List[CandidateDay]:
    result:List[CandidateDay] = []
    
    tz = ZoneInfo("Asia/Tokyo")

    end_date = start_date + timedelta(days=duration_days)
    required_slots = insert_event.duration // slot_minutes  # e.g. 120 / 30 = 4

    for n in range((end_date.date() - start_date.date()).days + 1):
        current_date = start_date.date() + timedelta(days=n)
        candidate_slots = []
        if current_date.weekday() < 5 and not jpholiday.is_holiday(current_date):  # 平日かつ祝日でない
            for hour in range(start_hour, end_hour):
                if hour >= lunch_start_hour and hour <= lunch_end_hour:
                    continue
                for minute in (0, 30):
                    start_time = datetime.combine(current_date, time(hour, minute, tzinfo=tz))
                    end_time = start_time + timedelta(minutes=slot_minutes * required_slots)

                    if end_time.time() <= time(end_hour, 0):
                        if is_slot_available((start_time, end_time), existing_events):
                            candidate_slots.append(Slot(start=start_time, end=end_time))
            result.append(CandidateDay(date=current_date, day_of_week=current_date.weekday(), candidates=candidate_slots))
    return result


            
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
# 候補日の取得
def get_candidate_days(trend: EventTrend, candidates: List[CandidateDay],max_candidates_per_day:int=3) -> List[CandidateDay]:
    

    result:List[CandidateDay] = []
    for candidate_day in candidates:
        print("candidate_day",len(candidate_day.candidates))
        print("candidate_day",candidate_day.candidates)
        slot_list: List[Slot] = []
        filtered_candidates = candidate_day.candidates
        # 曜日チェック
        busy_day = next((slot for slot in trend.busy_slots if slot.day == candidate_day.day_of_week), None)
        # 繁忙曜日と重複している場合
        if busy_day:
            filter_start = datetime.fromisoformat(f"{candidate_day.date}T{busy_day.start}:00+09:00")
            filter_end = datetime.fromisoformat(f"{candidate_day.date}T{busy_day.end}:00+09:00")
            filtered_candidates = [
                slot for slot in candidate_day.candidates
                if slot.end <= filter_start or
                slot.start >= filter_end
            ]
        for frequent_slot in trend.frequent_slots:
            filter_start = datetime.fromisoformat(f"{candidate_day.date}T{frequent_slot.start}:00+09:00")
            filter_end = datetime.fromisoformat(f"{candidate_day.date}T{frequent_slot.end}:00+09:00")
            for slot in filtered_candidates:
                if slot.start == filter_start:
                    slot_list.append(slot)
                    filtered_candidates.remove(slot)
                    if len(slot_list) == max_candidates_per_day: break
        
        for slot in filtered_candidates:
            slot_list.append(slot)
            if len(slot_list) == max_candidates_per_day: break
        
        candidate_day.candidates = slot_list
        result.append(candidate_day)
    return result