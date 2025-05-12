# main.py

import os
from dataclasses import dataclass
from dotenv import load_dotenv

from agents import Agent, set_tracing_disabled, RunContextWrapper, function_tool
from agents import OpenAIChatCompletionsModel, AsyncOpenAI

load_dotenv()  # loads GEMINI_API_KEY

# 1) Define the user‐context structure
@dataclass
class UserInfo:
    name: str
    age: int
    location: str
    interests: list
    preferences: dict

# 2) Expose the context‐reader as a tool
@function_tool
async def get_user_info(wrapper: RunContextWrapper[UserInfo]) -> str:
    u = wrapper.context
    return (
        f"User Info:\n"
        f"- Name: {u.name}\n"
        f"- Age: {u.age}\n"
        f"- Location: {u.location}\n"
        f"- Interests: {u.interests}\n"
        f"- Preferences: {u.preferences}"
    )

# 3) Configure the OpenAI/Vertex provider
Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)

# 4) Build the agent, **passing in both tools AND context**
async def ai_agent():
    set_tracing_disabled(True)

    user_info = UserInfo(
        name="Mustafa Mirza",
        age=18,
        location="Sialkot, Pakistan",
        interests=["reading", "traveling", "coding"],
        preferences={"language": "Punjabi & Urdu", "timezone": "EST"}
    )

    agent = Agent[UserInfo](
        name="Customer Support Assistant",
        instructions=("""
You are a professional customer support assistant.
Whenever the user asks about their personal details (name, age, location, interests, preferences),
you MUST call the function get_user_info() and then reply using exactly the data it returns.
"""
        ),
        model=model,
        tools=[get_user_info],     # allow calling get_user_info
               # <-- ***IMPORTANT: pass user_info here***
    )

    return agent , user_info
