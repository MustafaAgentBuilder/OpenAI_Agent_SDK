from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail, input_guardrail
import asyncio

# Pydantic model for guardrail output
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# Guardrail agent to check if input is math homework
guardrail_agent = Agent(
    name="Math Homework Check",
    instructions="Check if the user input is asking for math homework help.",
    output_type=MathHomeworkOutput
)

# Guardrail function
@input_guardrail
async def math_homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework
    )

# Main agent for handling user requests
main_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. Help users with their queries unless it's math homework.",
    input_guardrails=[InputGuardrail(guardrail_function=math_homework_guardrail)]
)

# Main function to run the agent
async def main():
    try:
        # Test with non-math input
        result = await Runner.run(main_agent, "How can I reset my password?")
        print("Result:", result.final_output)

        # Test with math homework input
        result = await Runner.run(main_agent, "Solve 2x + 3 = 7 for x.")
        print("Result:", result.final_output)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())