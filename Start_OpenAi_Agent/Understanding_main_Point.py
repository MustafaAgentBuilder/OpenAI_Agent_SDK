# The Agent and Runner classes help you build AI assistants.
# OpenAIChatCompletionsModel handles generating chat responses,
# and AsyncOpenAI is used to make API calls to the language model.
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from dotenv import load_dotenv 
import os
import asyncio

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

# ------------------------------
# Understanding Functions:
# ------------------------------
# Synchronous (sync) functions:
#   - They run one after the other.
#   - Each function finishes completely before the next one starts.
#   - Example: 
#         make_coffee() -> eat_breakfast() -> drive_to_work()
#
# Asynchronous (async) functions:
#   - They allow you to run tasks at the same time.
#   - They can pause when waiting (like during file reads or network calls),
#     so other tasks can run in the meantime.
#   - Example:
#         start_laundry() -> while laundry is running, prepare_dinner() -> while dinner cooks, answer_emails()

# ------------------------------
# Runner Methods:
# ------------------------------
# run() - An asynchronous method:
#   - Use it with 'await' inside an async function.
#   - Example: response = await Runner.run(agent, input="Your query here")
#
# run_sync() - A synchronous method:
#   - You can call it directly without 'await'.
#   - Example: response = Runner.run_sync(agent, input="Your query here")
#
# run_streamed() - A streaming response method:
#   - It gives you parts of the response as soon as they are ready.
#   - Example:
#         async for event in Runner.run_streamed(agent, input="Your query here").stream_events():
#             if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#                 print(event.data.delta, end="", flush=True)

# ------------------------------
# Example using run_sync()
# ------------------------------
def run():
    agent = Agent(
        name="Assistant", 
        instructions="You are a helpful assistant",
        model=model
    )
    # run_sync runs the agent synchronously and prints the final answer.
    result = Runner.run_sync(agent, "Tell me about Pak Army.")
    print(result.final_output) 

# ------------------------------
# Example using run() in an async function
# ------------------------------
async def new():
    agent = Agent(
        name="Assistant",
        instructions="You will respond to user queries.", 
        model=model
    )
    # run is asynchronous, so we use 'await' to get the response.
    response = await Runner.run(starting_agent=agent, input="Tell me about yourself?")
    print(response.final_output)

# Run the async function
asyncio.run(new())


# ------------------------------
# Example using run_streamed() for streaming responses
# ------------------------------
async def stream_example():
    agent = Agent(
        name="Assistant", 
        instructions="You will respond to user queries.", 
        model=model
    )
    # run_streamed returns parts of the answer as they are ready.
    result = Runner.run_streamed(starting_agent=agent, input="Tell me a short story")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

# # Run the streaming example
# asyncio.run(stream_example())