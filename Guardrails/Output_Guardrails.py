from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, OutputGuardrail, output_guardrail
import asyncio

# Pydantic model for guardrail output
class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

# Pydantic model for agent output
class MessageOutput(BaseModel):
    response: str

# Guardrail agent to check output
guardrail_agent = Agent(
    name="Math Output Check",
    instructions="Check if the output contains math-related content.",
    output_type=MathOutput
)

# Output guardrail function
@output_guardrail
async def math_output_guardrail(ctx, agent, output: MessageOutput):
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math
    )

# Main agent
main_agent = Agent(
    name="Response Agent",
    instructions="Respond to user queries.",
    output_type=MessageOutput,
    output_guardrails=[OutputGuardrail(guardrail_function=math_output_guardrail,name="Agent")]
)

# Main function
async def main():
    try:
        # Test with non-math output
        result = await Runner.run(main_agent, "Tell me about the weather.")
        print("Result:", result.final_output.response)

        # Test with math output
        result = await Runner.run(main_agent, "What is 2 + 2?")
        print("Result:", result.final_output.response)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())