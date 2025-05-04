from pydantic import BaseModel
from datetime import datetime
from util.common import UserInfo

class CalenderEventFilterParams(BaseModel):
    start_date: datetime  
    duration: int
    