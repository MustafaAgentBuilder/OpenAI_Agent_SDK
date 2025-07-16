from agents import (
    Agent,
    Runner,
    handoff,
    HandoffInputData,
    HandoffInputFilter,
    set_tracing_disabled,
    function_tool,
    MessageOutputItem,
)

from agents.items import ResponseOutputMessage
from agents.extensions.models.litellm_model import LitellmModel
from agents.items import ResponseOutputMessage
from dotenv import load_dotenv
import os
import asyncio

# ─── Load and check API key ─────────────────────────────────────────────────────
load_dotenv()
set_tracing_disabled(True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError(
        "GROQ_API_KEY environment variable is not set. Please set it in your .env file."
    )

# ─── Model setup ────────────────────────────────────────────────────────────────
model = LitellmModel(
    model="groq/qwen-qwq-32b",
    api_key=api_key
)

# ─── Weather tool ───────────────────────────────────────────────────────────────
@function_tool(

)
async def weather(city: str) -> str:
    """
    Dummy weather tool that returns a simple weather response for a given city.
    """
    return f"The weather in {city} is sunny and pleasant today."

# ─── Weather Agent ──────────────────────────────────────────────────────────────
weather_agent = Agent(
    name="Weather Agent",
    instructions=(
        "You are a specialized Weather Agent. "
        "Provide friendly, accurate weather info for any city. "
        "Use the `weather` tool to get forecasts."
    ),
    model=model,
    tools=[weather]
)

# def summary_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
#     # 1. Remove any tool‐related messages
#     filtered_data = handoff_filters.remove_all_tools(handoff_message_data)

#     # 2. Extract the last three messages (turns) from the history
#     history = filtered_data.input_history
#     if isinstance(history, tuple):
#         history = list(history)
#     last_three = history[-3:]

#     # 3. Build a summary string from those last three items
#     summary_text = " ".join(str(msg) for msg in last_three)

#     # 4. Wrap the summary text in a ResponseOutputMessage
#     summary_output = ResponseOutputMessage(summary_text)

#     # 5. Create a MessageOutputItem for the next agent to consume
#     summary_item = MessageOutputItem(
#         agent=weather_agent,     # or whichever agent you’re handing off to
#         raw_item=summary_output
#     )

#     # 6. Return a new HandoffInputData with only the summary
#     return HandoffInputData(
#         input_history=tuple(last_three),
#         pre_handoff_items=tuple(filtered_data.pre_handoff_items),
#         new_items=(summary_item,),
#     )

# ─── Main Agent ─────────────────────────────────────────────────────────────────
main_agent = Agent(
    name="Main Agent",
    instructions=(
        "You are the primary assistant. "
        "Help users with all questions. "
        "If they ask about weather, hand off to the Weather Agent."
    ),
    model=model,
    handoffs=[
        handoff(
            weather_agent,
            tool_name_override="Weather Agent Tool",
            tool_description_override="Provides current weather for any city.",
            input_filter=summary_handoff_message_filter,
        )
    ]
)

# ─── Demo runner ────────────────────────────────────────────────────────────────
async def Demo():
    result = await Runner.run(
        main_agent,
        input="What is the weather like in New York today?",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(Demo())
