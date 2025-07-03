
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    FunctionTool,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    enable_verbose_stdout_logging
)
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
import os
import asyncio

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

# ✅ 3. Weather Tool
async def get_current_weather_func(ctx: RunContextWrapper, args: dict) -> str:
    city = args["city"]
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

async def get_current_time(ctx: RunContextWrapper, args: dict) -> Time:
    city = args["city"]
    return Time(city=city, time="12:00 PM")  # Dummy fixed time

time_tool = FunctionTool(
    name="get_current_time",
    description="Get the current time for a given city.",
    params_json_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city to get the time for"},
        },
        "required": ["city"],
    },
    on_invoke_tool=get_current_time,
    strict_json_schema=True,
    is_enabled=True,
)

# ✅ 5. User Info Tool
class UserInfo(BaseModel):
    name: str
    age: int

user_registry: dict[str, UserInfo] = {}

def check_user_info_valid(ctx: RunContextWrapper, args: dict) -> bool:
    try:
        user_info = UserInfo.model_validate(args)
        return bool(user_info.name and isinstance(user_info.age, int) and user_info.age > 0)
    except Exception:
        return False

async def get_user_info(ctx: RunContextWrapper, args: dict) -> UserInfo:
    parsed = UserInfo.model_validate(args)

    request_type = getattr(ctx, "request_type", None)
    requested_name = getattr(ctx, "requested_name", None)

    if request_type == "get_info" and requested_name:
        user = user_registry.get(requested_name)
        if user:
            return user
        else:
            raise ValueError(f"No user found with name '{requested_name}'.")

    if check_user_info_valid(ctx, args):
        user_registry[parsed.name] = parsed
        return parsed
    else:
        raise ValueError("Invalid user information provided.")

def user_info_is_enabled(ctx: RunContextWrapper, agent: Agent) -> bool:
    user = getattr(ctx, "user", None)
    return user in ["Alice", "admin"]

user_info_tool = FunctionTool(
    name="user_info",
    description="Get or register user information",
    params_json_schema=UserInfo.model_json_schema(),
    on_invoke_tool=get_user_info,
    strict_json_schema=True,
    is_enabled=user_info_is_enabled,
)

# ✅ 6. Create the Agent
agent = Agent(
    name="assistant",
    model=model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[get_current_weather, time_tool, user_info_tool],
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
