from features.map.schemas import CalculateTravelTimeParams, CalculateTravelTimeResponse
from features.map.main import get_travel_time
from chains.company.models import TravelTimeResult
async def get_travel_time_chain(inputs):
    """
    出発地点と目的地を指定して、移動時間を計算する
    """
    print("get_travel_time_chain",inputs)
    user_info = inputs["user_info"]
    location = inputs["address"] if inputs["address"] else inputs["info"].location
    params = CalculateTravelTimeParams(
        origin=user_info.location,
        destination=location,
        mode="DRIVING"
    )
    response = await get_travel_time(params)
    return TravelTimeResult(
        start_address=response.start_address,
        end_address=response.end_address,
        distance_text=response.distance_text,
        duration_text=response.duration_text,
        duration_seconds=response.duration_seconds
    )
