import os
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, trace
from dotenv import load_dotenv
import agentops

# Load environment variables
load_dotenv()

# Initialize AgentOps
agentops.init(os.getenv("AGENTOPS_API_KEY"))

# Define the model name
MODEL_NAME = os.getenv("gemini-1.5-flash")

async def main():
    agent = Agent(
        name="AssistanceAgent",
        instructions="Assist the user with their questions",
        model=MODEL_NAME
    )

    with trace(workflow_name="Example workflow"):
        first_result = await Runner.run(agent, "Start the task")
        second_result = await Runner.run(agent, f"Rate this result: {first_result.final_output}")
        print(f"Result: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
