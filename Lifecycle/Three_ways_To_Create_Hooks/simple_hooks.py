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



async def on_start(ctx: RunContextWrapper[Any], agent: Agent) -> None:
    print(f"Started {agent.name} – session: {ctx.context}, role: {ctx.context}")


async def on_end(ctx: RunContextWrapper[Any], agent: Agent, output: Any) -> None:
    print(f"Ended {agent.name} with output: {output}")


async def on_handoff(context: RunContextWrapper[Any], agent: Agent, source: Agent) -> None:
    print(f"Handoff from {source.name} to {agent.name} in session {context.context.session_id}")
    # return await super().on_handoff(context, agent, source)

agent = Agent[Any](
    name="ProAgent",
    instructions="Fetch and present data cleanly",
    hooks=AgentHooks(
    ),
    model=model
)


agent.hooks.on_start = on_start
agent.hooks.on_end = on_end
agent.hooks.on_handoff = on_handoff
async def main():
    result = await Runner.run(
        agent,
        input="Fetch info on sales figures",
        context={"session_id": "abc123", "user_role": "student"}
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())