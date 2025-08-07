# This code is part of the Agent with UI project.

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv 
import os
import asyncio

load_dotenv()
set_tracing_disabled(True)

Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)

async def stream_events():
    agent = Agent(
        name="Customer Support Assistant", 
        instructions="""You are a professional customer support assistant with expertise in helping users.
- Respond with accurate, helpful, and concise information
- Be polite and empathetic to user concerns
- Ask clarifying questions when needed to better understand the query
- Provide step-by-step guidance for complex problems
- Use a friendly, professional tone throughout the conversation
- When you don't know something, admit it instead of making up information
- Summarize key points at the end of longer responses
""", 
        model=model
    )
  

    return agent
