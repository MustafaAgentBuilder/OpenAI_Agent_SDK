import asyncio
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel
# Load your Gemini key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in your environment")

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    set_tracing_disabled
)
set_tracing_disabled(True)
# Define your output schema
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# The little “homework‐detector” agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=LitellmModel(model="gemini/gemini-1.5-flash", api_key=API_KEY)
)

# Our input guardrail
@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

# Your main agent
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
    model=LitellmModel(model="gemini/gemini-1.5-flash", api_key=API_KEY)
)

# The async entry point
async def main():
    while True:
        # Get user input
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        # Run the agent with the user input
        try:
            result = await Runner.run(agent, user_input)
            print(f"Agent response: {result.final_output}")

        except InputGuardrailTripwireTriggered:
            print("Guardrail tripwire triggered - math homework detected")
    # j
if __name__ == "__main__":
    asyncio.run(main())
