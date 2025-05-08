from pydantic import BaseModel

class CalculateTravelTimeParams(BaseModel):
    origin: str
    destination: str
    mode: str

class CalculateTravelTimeResponse(BaseModel):
    start_address: str
    end_address: str
    distance_text: str
    duration_text: str
    duration_seconds: int
