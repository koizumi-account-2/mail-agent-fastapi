import requests
from modules.config import GOOGLE_MAP_API_KEY
from features.map.schemas import CalculateTravelTimeParams,CalculateTravelTimeResponse
async def get_travel_time(inputs: CalculateTravelTimeParams) -> CalculateTravelTimeResponse:
    api_key = GOOGLE_MAP_API_KEY    
    params = {
        "origin": inputs.origin,
        "destination": inputs.destination,
        "mode": inputs.mode,
        "language": "ja",
        "key": api_key
    }
    url = "https://maps.googleapis.com/maps/api/directions/json"
    res = requests.get(url, params=params).json()
    leg = res["routes"][0]["legs"][0]
    return CalculateTravelTimeResponse(
        start_address=leg["start_address"],
        end_address=leg["end_address"],
        distance_text=leg["distance"]["text"],
        duration_text=leg["duration"]["text"],
        duration_seconds=leg["duration"]["value"],
    )


# transit
