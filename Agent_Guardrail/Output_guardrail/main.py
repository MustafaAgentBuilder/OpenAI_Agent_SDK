import asyncio
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel

# 1. Load your Gemini key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in your environment")

# 2. Import Agents SDK pieces, including the output guardrail decorator
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    output_guardrail,
    set_tracing_disabled,
)
set_tracing_disabled(True)

# 3. Define the schema the guardrail-agent returns
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# 4. Tiny “homework‐detector” agent that flags math questions
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Decide if this output looks like I'm doing math homework for a student.",
    output_type=MathHomeworkOutput,
    model=LitellmModel(model="gemini/gemini-1.5-flash", api_key=API_KEY),
)

# 5. The **output** guardrail function
@output_guardrail
async def math_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    # Run the small guardrail_agent on the agent’s own output
    result = await Runner.run(guardrail_agent, output, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

# 6. Your main agent, now with an output guardrail
agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_output_guardrail],
    model=LitellmModel(model="gemini/gemini-1.5-flash", api_key=API_KEY),
)

# 7. Async REPL entry point
async def main():
    while True:
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        try:
            # Run the agent and get its final reply
            result = await Runner.run(agent, user_input)
            print(f"Agent response: {result.final_output}")

        except OutputGuardrailTripwireTriggered:
            # If the agent’s reply looked like “doing math homework,” we get here
            print("Guardrail tripwire triggered — the agent tried to do math homework!")

if __name__ == "__main__":
    asyncio.run(main())
