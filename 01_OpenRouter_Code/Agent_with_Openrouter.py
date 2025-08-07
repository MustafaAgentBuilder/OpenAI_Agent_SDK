# Easy to write and make Agent
# Import necessary libraries and modules
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled  # Import agent-related classes
from openai import AsyncOpenAI  # Import OpenAI's async client
from dotenv import load_dotenv  # For loading environment variables from .env file
import os  # For accessing environment variables
import asyncio  # For running asynchronous code


# Load environment variables from .env file
load_dotenv()
# Disable tracing for better performance
set_tracing_disabled(True)

# Get configuration from environment variables
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")  # Get API key
openrouter_model = os.getenv("MODEL")  # Get model name
openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")  # Get API base URL

# Check if API key exists
if openrouter_api_key is None:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")  # Stop execution if no API key

# Create an OpenAI client configured for OpenRouter
provider = AsyncOpenAI(
    api_key=openrouter_api_key,  # Set the API key
    base_url=openrouter_base_url,  # Set the custom base URL for OpenRouter
)

# Main function that runs our agent
async def main():
    # Print configuration values for debugging
    # print(f"API Key: {openrouter_api_key}, Model: {openrouter_model}, Base URL: {openrouter_base_url}")
    
    # Create a new Agent instance with specific instructions
    agent = Agent(
        name="Teacher",  # Name for the agent
        instructions="You are a helpful assistant. Answer the user's questions.",  # Instructions for how the agent should behave
        model=OpenAIChatCompletionsModel(  # Set up the model to use
            model=openrouter_model,  # Use the model name from environment variables
            openai_client=provider  # Use our configured OpenRouter client
        )
    )
    
    # Run the agent with a specific input question
    response = await Runner.run(
        starting_agent=agent,  # Use the agent we created above
        input="What is the meaning of life?",  # The question to ask the agent
    )
    
    # Print the agent's response to the terminal
    print(response.final_output)

# This code runs only when the script is executed directly (not imported)
if __name__ == "__main__":
    asyncio.run(main())  # Run the main async function with asyncio