import os
from dataclasses import dataclass
from dotenv import load_dotenv

from agents import Agent, set_tracing_disabled, RunContextWrapper, function_tool
from agents import OpenAIChatCompletionsModel, AsyncOpenAI

load_dotenv()  # loads GEMINI_API_KEY

# 1) Define the user-context structure
@dataclass
class UserInfo:
    name: str
    age: int
    location: str
    interests: list
    preferences: dict

# 2a) Expose the context-reader as a tool
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

# 2b) Expose setter tools for each field
@function_tool
async def set_user_name(wrapper: RunContextWrapper[UserInfo], name: str) -> str:
    wrapper.context.name = name
    return f"Okay, I’ll remember that your name is {name}."

@function_tool
async def set_user_age(wrapper: RunContextWrapper[UserInfo], age: int) -> str:
    wrapper.context.age = age
    return f"Got it—your age is now set to {age}."

@function_tool
async def set_user_location(wrapper: RunContextWrapper[UserInfo], location: str) -> str:
    wrapper.context.location = location
    return f"Sure—your location is now {location}."

@function_tool
async def add_user_interest(wrapper: RunContextWrapper[UserInfo], interest: str) -> str:
    wrapper.context.interests.append(interest)
    return f"Added interest: {interest}."

@function_tool
async def set_user_preference(wrapper: RunContextWrapper[UserInfo], key: str, value: str) -> str:
    wrapper.context.preferences[key] = value
    return f"Set preference {key} to {value}."

# 3) Configure the OpenAI/Vertex provider
Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)

# 4) Build the agent factory (returns both agent & context)
async def ai_agent():
    set_tracing_disabled(True)

    # Initial (blank) context
    user_info = UserInfo(
        name="Unknown",
        age=0,
        location="Unknown",
        interests=[],
        preferences={}
    )

    agent = Agent[UserInfo](
        name="Customer Support Assistant",
        instructions="""
You are a professional customer support assistant.

1. When the user provides personal details, identify each piece of information separately and call the corresponding setter tool for each:
   - If the user mentions their name (e.g., “My name is X.”), call set_user_name(name=X)
   - If the user mentions their age (e.g., “I’m N years old.”), call set_user_age(age=N)
   - If the user mentions their location (e.g., “I live in L.”), call set_user_location(location=L)
   - If the user mentions an interest (e.g., “I like I.” or “My interests include I.”), call add_user_interest(interest=I)
     (Call this tool for each interest if multiple are mentioned.)
   - If the user mentions a preference (e.g., “My preference for K is V.”), call set_user_preference(key=K, value=V)
     (Call this tool for each key-value pair if multiple are mentioned.)

2. Important: If the user provides multiple details in one message (e.g., “My name is X, I’m N years old, and I live in L.”), process each detail separately by calling the appropriate tool for each piece of information. Do not combine multiple updates into a single tool call.

3. When the user asks “What’s my name/age/location/interests/preferences?” or “Tell about me,” call get_user_info() and respond exactly with the data it returns.

Do not answer personal-info questions directly—always invoke the appropriate tool first.
""",
        model=model,
        tools=[
            get_user_info,
            set_user_name,
            set_user_age,
            set_user_location,
            add_user_interest,
            set_user_preference
        ],
    )

    return agent, user_info