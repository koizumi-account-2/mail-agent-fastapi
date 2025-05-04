from datetime import datetime, timedelta
import jpholiday
def get_weekdays(start: datetime,days: int) -> list[datetime]:
    """
    指定された日付から指定された日数後の日付を返す
    """
    weekdays = []
    for i in range(days):
        current = start + timedelta(days=i)
        if current.weekday() < 5 and not jpholiday.is_holiday(current):
            weekdays.append(current)
    return weekdays
