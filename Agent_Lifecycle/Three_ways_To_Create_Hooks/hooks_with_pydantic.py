from agents import Agent, AgentHooks, Runner, RunContextWrapper , set_tracing_disabled , OpenAIChatCompletionsModel 
import asyncio
import os
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import Any

set_tracing_disabled(True)
load_dotenv()


Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completion model with the API provider.
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)

class MyContext(BaseModel):
    session_id: str
    user_role: str

class ProHook(AgentHooks[MyContext]):
    async def on_start(self, ctx: RunContextWrapper[MyContext], agent:Agent):
        print(f"Started {agent.name} – session: {ctx.context.session_id}, role: {ctx.context.user_role}")

    async def on_end(self, ctx, agent, output):
        print(f"Ended {agent.name} with output: {output}")

    
    async def on_handoff(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], source: Agent[MyContext]) -> None:
        print(f"Handoff from {source.name} to {agent.name} in session {context.context.session_id}")
        return await super().on_handoff(context, agent, source)
    


hooks = ProHook()
hooks.on_start
hooks.on_end
hooks.on_handoff
agent = Agent[MyContext](
    name="ProAgent",
    instructions="Fetch and present data cleanly",
    hooks=hooks,
    model=model
)

# If running asynchronously:
import asyncio

async def main():
    result = await Runner.run(
        agent,
        input="Fetch info on sales figures",
        context=MyContext(session_id="abc123", user_role="student")
    )
    print("Final Output:", result.final_output)

asyncio.run(main())