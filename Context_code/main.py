# LLM Context: Info sent to the AI model (like chat history or instructions) to generate smart replies.
# Local Context: Data the agent’s code uses internally (like user settings or tool data), not sent to the AI model.
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    user_info = UserInfo(name="John", uid=123)

# In LLm Context 
# We instruction Parameter In Our agent class to use the function tool fetch_user_age.
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output)  
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())


import asyncio
from dataclasses import dataclass
from typing import List

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

@function_tool
async def fetch_user_info(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} has ID {wrapper.context.uid}"

async def main():
    user_info = UserInfo(name="John", uid=123)

    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age, fetch_user_info],
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="What is the age and info of the user?",
        context=user_info,
    )

    print(result.final_output)  

if __name__ == "__main__":
    asyncio.run(main())