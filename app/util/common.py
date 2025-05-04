from fastapi import Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from chains.calendar.models import EventTrend
def get_access_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    return authorization.replace("Bearer ", "")

class UserInfo(BaseModel):
    location: str = Field(..., description="ユーザーの住所。ここから距離が計算されます")
    event_trend: Optional[EventTrend] = Field(None, description="ユーザーのイベントの傾向")