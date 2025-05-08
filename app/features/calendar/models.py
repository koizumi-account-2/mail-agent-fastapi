from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime, date
from typing import List

class CalenderEventFilterParams(BaseModel):
    start_date: datetime  
    duration: int
    


class Slot(BaseModel):
    start: datetime
    end: datetime

class CandidateDay(BaseModel):
    date: date
    day_of_week: int # 0:月曜日,1:火曜日,2:水曜日,3:木曜日,4:金曜日,5:土曜日,6:日曜日
    candidates: List[Slot]