import os
import asyncio
from agents import AsyncOpenAI
from agents import Agent, Runner, trace,OpenAIChatCompletionsModel
import agentops
from dotenv import load_dotenv
load_dotenv()

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model = "gemini-1.5-flash"
)
agentops.init(os.getenv("Agenttops_api_key"))

# Initialize AgentOps,

# Define the model name,
async def main():
    agent = Agent(
        name="AssistanceAgent",
        instructions="Assist the user with their questions",
        model=model,
    )

    with trace(workflow_name="Example workflow"):
        first_result = await Runner.run(agent, "Start the task")
        second_result = await Runner.run(agent, f"Rate this result: {first_result.final_output}")
        print(f"Result: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

# if name == "main":
asyncio.run(main())