import os
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, set_default_openai_api, set_default_openai_client, set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from pprint import pprint
import asyncio
from dotenv import load_dotenv

load_dotenv()

from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

BASE_URL =  "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"


if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )



client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

set_default_openai_client(client=client, use_for_tracing=True)
set_default_openai_api("chat_completions")
# set_tracing_disabled(disabled=True)


# Custom trace processor to collect trace data locally
class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started: {trace.trace_id}")

    def on_trace_end(self, trace):
        print(f"Trace ended: {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)
        print("*"*20)
        print(f"Span started: {span.span_id}")
        print(f"Span details: ")
        pprint(span.export())

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(f"Span details:")
        pprint(span.export())

    def force_flush(self):
        print("Forcing flush of trace data")

    def shutdown(self):
        print("=======Shutting down trace processor========")
        # Print all collected trace and span data
        print("Collected Traces:")
        for trace in self.traces:
            print(trace.export())
        print("Collected Spans:")
        for span in self.spans:
            print(span.export())


if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code.")

# Create OpenAI client
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# Set up the custom trace processor
local_processor = LocalTraceProcessor()
set_trace_processors([local_processor])

# Example function to run an agent and collect traces
async def main():
    agent = Agent(name="AssistanceAgent", instructions="Assist the user with their questions", model=MODEL_NAME)

    with trace("Example workflow"):
        first_result = await Runner.run(agent, "Start the task")
        second_result = await Runner.run(agent, f"Rate this result: {first_result.final_output}")
        print(f"Result: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

# Run the main function
asyncio.run(main())