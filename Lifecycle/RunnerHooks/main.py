from agents import Agent, AgentHooks, Runner, RunContextWrapper
import asyncio
from typing import Any

# Custom context class
class MyContext:
    def __init__(self, session_id: str):
        self.session_id = session_id

# Runner ke liye global hooks class
class MyRunnerHooks(AgentHooks[MyContext]):
    def on_agent_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext]) -> None:
        print(f"[Runner] Agent {agent.name} started! Session ID: {context.context.session_id}")

    def on_agent_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], output: Any) -> None:
        print(f"[Runner] Agent {agent.name} ended! Output: {output}")

    def on_handoff(self, context: RunContextWrapper[MyContext], from_agent: Agent[MyContext], to_agent: Agent[MyContext]) -> None:
        print(f"[Runner] Handoff from {from_agent.name} to {to_agent.name}")

    def on_tool_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any) -> None:
        print(f"[Runner] Tool {tool.name} started by {agent.name}")

    def on_tool_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any, result: str) -> None:
        print(f"[Runner] Tool {tool.name} ended! Result: {result}")

# Simple tool function
def get_info() -> str:
    return "Sample Information"

# Agents
data_agent = Agent[MyContext](
    name="DataAgent",
    instructions="You fetch information",
    tools=[get_info]
)

triage_agent = Agent[MyContext](
    name="TriageAgent",
    instructions="Handoff to DataAgent for info requests",
    handoffs=[data_agent]
)

# Main async function
async def main():
    context = MyContext(session_id="session_001")
    runner = Runner(hooks=MyRunnerHooks())
    result = await runner.run(triage_agent, input="Get some info", context=context)
    print(f"Final Output: {result.final_output}")

# Run the program
if __name__ == "__main__":
    asyncio.run(main())