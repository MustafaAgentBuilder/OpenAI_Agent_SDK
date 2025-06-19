from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail
from pydantic import BaseModel
import asyncio

# Pydantic model for guardrail output
class ValidQueryOutput(BaseModel):
    is_valid: bool
    reasoning: str

# Guardrail agent to check if input is a valid question
guardrail_agent = Agent(
    name="GuardrailAgent",
    instructions="Check if the input is a valid question about geography.",
    output_type=ValidQueryOutput
)

# Guardrail function
async def geography_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(ValidQueryOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_valid
    )

# Tool agent to fetch capital city
tool_agent = Agent(
    name="CapitalToolAgent",
    instructions="Return the capital city of the given country.",
    tools=[{
        "name": "get_capital",
        "description": "Fetches the capital city of a country",
        "parameters": {"type": "object", "properties": {"country": {"type": "string"}}}
    }]
)

# Main agent that handles geography questions and may hand off to tool agent
main_agent = Agent(
    name="GeographyAgent",
    instructions="Answer geography-related questions or hand off to a tool agent.",
    input_guardrails=[InputGuardrail(guardrail_function=geography_guardrail)]
)

# Async function to run the agent
async def main():
    try:
        # Run the main agent with an input
        input_query = "What is the capital of Brazil?"
        result = await Runner.run(main_agent, input_query)

        # Exploring RunResultBase components
        print("=== RunResultBase Components ===")
        print(f"Final Output: {result.final_output}")
        print(f"Input Guardrail Results: {result.input_guardrail_results}")
        print(f"Output Guardrail Results: {result.output_guardrail_results}")
        print(f"Raw Responses: {result.raw_responses}")
        print(f"Last Agent: {result.last_agent.name if result.last_agent else 'None'}")
        print(f"To Input List: {result.to_input_list()}")

        # Check for HandoffOutputItem
        handoff_found = False
        for item in result.to_input_list():
            if hasattr(item, 'source') and hasattr(item, 'target'):
                handoff_found = True
                print(f"\nHandoffOutputItem Detected:")
                print(f"Source Agent: {item.source}")
                print(f"Target Agent: {item.target}")
        
        if not handoff_found:
            print("\nNo HandoffOutputItem detected.")

        # Check for ToolCallItem and ToolCallOutputItem
        tool_call_found = False
        tool_output_found = False
        for item in result.to_input_list():
            if hasattr(item, 'tool_call_id'):
                if not hasattr(item, 'output'):
                    tool_call_found = True
                    print(f"\nToolCallItem Detected:")
                    print(f"Tool Name: {item.tool_name}")
                else:
                    tool_output_found = True
                    print(f"\nToolCallOutputItem Detected:")
                    print(f"Tool Output: {item.output}")

        if not tool_call_found:
            print("No ToolCallItem detected.")
        if not tool_output_found:
            print("No ToolCallOutputItem detected.")

        # Check for ReasoningItem
        reasoning_found = False
        for item in result.to_input_list():
            if hasattr(item, 'type') and item.type == 'reasoning':
                reasoning_found = True
                print(f"\nReasoningItem Detected:")
                print(f"Reasoning: {item.content}")

        if not reasoning_found:
            print("No ReasoningItem detected.")

    except Exception as e:
        print(f"Error: {e}")

# Run the async function
asyncio.run(main())



"""

=== RunResultBase Components ===
Final Output: Brasilia
Input Guardrail Results: {'is_valid': True, 'reasoning': 'This is a geography question'}
Output Guardrail Results: {'is_valid': True}
Raw Responses: [<ModelResponse object>]
Last Agent: CapitalToolAgent

To Input List: ['What is the capital of Brazil?', <HandoffOutputItem>, <ToolCallItem>, <ToolCallOutputItem>, <ReasoningItem>]

HandoffOutputItem Detected:
Source Agent: GeographyAgent
Target Agent: CapitalToolAgent

ToolCallItem Detected:
Tool Name: get_capital

ToolCallOutputItem Detected:
Tool Output: Brasilia

ReasoningItem Detected:
Reasoning: Checking the capital of Brazil using the get_capital tool.

"""