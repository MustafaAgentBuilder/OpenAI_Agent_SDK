from agents import Agent, AgentHooks, Runner, RunContextWrapper , set_tracing_disabled , OpenAIChatCompletionsModel 
import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import Any





# Load environment variables from a .env file
load_dotenv()

# Disable extra tracing/logging for cleaner output
set_tracing_disabled(True)

# This code is written by me to use this open-source SDK

# Create an API provider with AsyncOpenAI using your API key and base URL.
Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completion model with the API provider.
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)



# define context and hooks
class MyContext:
    def __init__(self, session_id: str):
        self.session_id =  session_id

# class MyHooks(AgentHooks[MyContext]):
    async def on_start(self, context, agent):
        print(f"#######[Runner] Agent {agent.name} started!")

    async def on_end(self, context, agent, output):
        print(f"#########[Runner] Agent {agent.name} ended! Output: {output}")

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"[Runner] Handoff from {from_agent.name} to {to_agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"[Runner] Tool {tool.name} started by {agent.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[Runner] Tool {tool.name} ended! Result: {result}")

# create agent correctly
new_hook = MyContext(session_id="12345")  # Example session ID, can be any string
# my_hook = MyHooks()
# # my_hook.session_id = "12345"  # Example session ID, can be any string
new_hook.on_end  
new_hook.on_handoff
new_hook.on_tool_start
new_hook.on_start
new_hook.on_tool_end


agent = Agent(
    name="AssistantAgent",
    instructions="You are a helpful assistant.",
    hooks=new_hook,  # Pass session_id to the hook,  # Pass session_id to the context
    model=model,
)
async def main():
    result = await Runner.run(
        agent,
        input="Please fetch data about X",
        # context=my_hook,
    )
    print("Final output:", result.final_output)

import asyncio
asyncio.run(main())
