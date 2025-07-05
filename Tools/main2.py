from agents import Agent , FunctionTool 
from pydantic import BaseModel



class Weather(BaseModel):
    location : str


async def get_weather(weather: Weather ) ->str:
    # Simulate a weather API call

    return f"Weather in {weather.location} is sunny"



tool = FunctionTool(
    name ="get_weather",
    description="You Feath the info form class",
    params_json_schema=Weather.model_json_schema(),
    on_invoke_tool=

)