from agents import Agent, AgentHooks, Runner, RunContextWrapper
import asyncio
from typing import Any

# Custom context class
class MyContext:
    def __init__(self, user_name: str):
        self.user_name = user_name

# Agent-specific hooks class
class MyAgentHooks(AgentHooks[MyContext]):
    def on_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext]) -> None:
        print(f"[Agent] {agent.name} started for user: {context.context.user_name}")

    def on_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], output: Any) -> None:
        print(f"[Agent] {agent.name} ended! Output: {output}")

    def on_handoff(self, context: RunContextWrapper[MyContext], from_agent: Agent[MyContext], to_agent: Agent[MyContext]) -> None:
        print(f"[Agent] Handoff from {from_agent.name} to {to_agent.name}")

    def on_tool_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any) -> None:
        print(f"[Agent] Tool {tool.name} started by {agent.name}")

    def on_tool_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any, result: str) -> None:
        print(f"[Agent] Tool {tool.name} ended! Result: {result}")

# Simple tool function
def process_data() -> str:
    return "Processed Data"

# Agent with specific hooks
info_agent = Agent[MyContext](
    name="InfoAgent",
    instructions="You process data",
    tools=[process_data],
    hooks=MyAgentHooks()
)

# Main async function
async def main():
    context = MyContext(user_name="Ali")
    result = await Runner.run(info_agent, input="Process some data", context=context)
    print(f"Final Output: {result.final_output}")

# Run the program
if __name__ == "__main__":
    asyncio.run(main())