from agents import Agent, Runner, ModelSettings, function_tool , OpenAIChatCompletionsModel , AsyncOpenAI, set_tracing_disabled 
from dotenv import load_dotenv 
import os
import asyncio
from dataclasses import asdict
from pprint import pprint

set_tracing_disabled(True)
load_dotenv()

Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completion model with the API provider.
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=Provider,
)


@function_tool
def add(a: int, b: int) -> int:
    return a + b




# In this code not comment setting are all run with Gemini or all Run with OpenAI

agent = Agent(
    name="Calculator",
    instructions="Use the add tool to perform addition.",
    model=model,
    model_settings=ModelSettings(
        temperature=0.0,
        top_p=1.0,
        # frequency_penalty=0.0,
        presence_penalty=0.0,
        tool_choice="auto",
        # parallel_tool_calls=True,
        truncation="auto",
        max_tokens=100,
        # metadata={"task":"math"},
        # store=True,
        include_usage=True,
        # extra_args={"logit_bias": {}}
    ),
    tools=[add],
)

result = Runner.run_sync(agent, "What is 12 + 30?")
# print("Answer:", result.final_output)
print("Result:")
pprint(asdict(result))


# pprint(asdict(result))