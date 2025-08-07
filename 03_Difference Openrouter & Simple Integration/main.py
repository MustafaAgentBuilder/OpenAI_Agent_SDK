"""
OpenRouter Agent Implementation Example

This script demonstrates how to use the 'agents' framework with OpenRouter
to easily access various AI models through a consistent interface.

Benefits:
- Higher-level abstraction through the Agent class
- Easy model switching by just changing the model name
- Asynchronous processing for better performance
- Structured agent behavior with instructions
"""

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables and configure settings
load_dotenv()
set_tracing_disabled(True)

# Configuration variables for OpenRouter
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = "https://openrouter.ai/api/v1"

# You can easily switch between different models by changing this variable
# Examples of free models you can use:
# "google/gemini-2.0-flash-lite-preview-02-05:free"
# "anthropic/claude-3-haiku:free"
# "nvidia/llama-3.1-nemotron-nano-8b-v1:free"
# "mistralai/mistral-7b-instruct:free"
openrouter_model = "google/gemini-2.0-flash-lite-preview-02-05:free"

# Verify that the API key is available
if not openrouter_api_key:
    raise ValueError("OpenRouter API key is missing. Please set OPENROUTER_API_KEY in your .env file.")

# Create the AsyncOpenAI client configured for OpenRouter
provider = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url=openrouter_base_url,
)

async def main():
    # Print configuration for debugging
    print(f"Using model: {openrouter_model}")
    print(f"OpenRouter base URL: {openrouter_base_url}")
    
    # Create an agent with specific behavior instructions
    agent = Agent(
        name="OpenRouter Assistant",
        instructions="You are a helpful AI assistant. Provide clear, concise answers to questions.",
        model=OpenAIChatCompletionsModel(
            model=openrouter_model,
            openai_client=provider
        )
    )
    
    # Define your input question or prompt
    user_question = "What are three interesting facts about space exploration?"
    
    # Run the agent and get response
    response = await Runner.run(
        starting_agent=agent,
        input=user_question,
    )
    
    # Display the result
    print("\nQuestion:", user_question)
    print("\nResponse:")
    print(response.final_output)

# Execute the main function when the script is run directly
if __name__ == "__main__":
    asyncio.run(main())



