from agents.tool_context import ToolContext
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    FunctionTool,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    enable_verbose_stdout_logging,
    function_tool,
    default_tool_error_function
)
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
import os
import asyncio
import json

# Load environment variables from .env file
load_dotenv()

# Optional: Show logs if you want
enable_verbose_stdout_logging()

# Disable tracing/logging (cleaner output)
set_tracing_disabled(True)

# ✅ 1. Set up the OpenAI provider (make sure your API key and base URL are correct!)
Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# ✅ 2. Connect the provider to a model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)



@function_tool(
    name_override="Addition",
    description_override="Adds two numbers together.",
    docstring_style="google",
    use_docstring_info=True,
    # Correct usage: pass a function that takes (ctx, error) as arguments
    # failure_error_function=lambda ctx, error: f"Error in add_numbers tool: {error}",
    failure_error_function=default_tool_error_function,
    strict_mode=True,
    is_enabled=True,
)

async def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
        int: The sum of the two numbers.
    """
    return a + b




# ✅ 3. Weather Tool
async def get_current_weather_func(ctx: ToolContext, args: str) -> str:
    args_dict = json.loads(args)
    city = args_dict["city"]
    return f"The weather in {city} is sunny."

get_current_weather = FunctionTool(
    name="get_current_weather",
    description="Get the current weather for a given city.",
    params_json_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city to get the weather for"},
        },
        "required": ["city"],
    },
    on_invoke_tool=get_current_weather_func,
    strict_json_schema=True,
)

# ✅ 4. Time Tool
class Time(BaseModel):
    city: str
    time: str

async def get_current_time(ctx: ToolContext, args: str) -> Time:
    """
    Returns the current time for a given city.

    Args:
        ctx (ToolContext): The tool context.
        args (str): A JSON string containing the city name.

    Returns:
        Time: An object containing the city and its current time.
    """
    args_dict = json.loads(args)
    city = args_dict.get("city")
    # For demonstration, we return a fixed time. Replace with real logic as needed.
    return Time(city=city, time="12:00 PM")

time_tool = FunctionTool(
    name="get_current_time",
    description="Get the current time for a given city.",
    params_json_schema=Time.model_json_schema(),
    on_invoke_tool=get_current_time,
    strict_json_schema=True,
    is_enabled=True,
)


# ✅ 6. Create the Agent
agent = Agent(
    name="assistant",
    model=model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[get_current_weather, time_tool, add_numbers] #user_info_tool],
    tool_use_behavior="stop_on_first_tool",
    reset_tool_choice=True,
)

# ✅ 7. Experiment Loop
async def experiment():
    while True:
        user_query = input("Enter your question: ")
        if user_query.strip() == "":
            print("No input entered. Exiting.")
            break
        result = await Runner.run(agent, user_query)
        print(result.final_output)

# ✅ 8. Run main loop
if __name__ == "__main__":
    asyncio.run(experiment())
