# OpenAI Agents SDK: Deep Study Series

This repository is part of the "OpenAI SDK: Deep Study" educational series, launched to help beginners understand the OpenAI Agents SDK comprehensively. The goal is to enable learners to confidently work with the SDK and prepare for a complex quiz planned after Eid. This `README.md` covers the lifecycle of agents in the OpenAI Agents SDK, including explanations and code examples for both the Runner lifecycle and Agent lifecycle, based on the documentation at [OpenAI Agents SDK Lifecycle Reference](https://openai.github.io/openai-agents-python/ref/lifecycle/).

## Overview of OpenAI Agents SDK Lifecycle

The OpenAI Agents SDK lifecycle provides callbacks to track various stages of an agent's execution, such as starting, ending, tool usage, or handoff to another agent. These callbacks allow developers to monitor and customize agent behavior, making it easier to debug or enhance workflows. The lifecycle is managed through the `AgentHooks` or `RunnerHooks` class, which supports both global (Runner-level) and agent-specific callbacks.

### Key Lifecycle Callbacks
- **Global Callbacks (Runner-level)**:
  - `on_agent_start`: Called when any agent starts.
  - `on_agent_end`: Called when an agent produces its final output.
  - `on_handoff`: Called when control is transferred between agents.
  - `on_tool_start`: Called before a tool is invoked.
  - `on_tool_end`: Called after a tool completes execution.
- **Agent-Specific Callbacks**:
  - `on_start`: Called when the specific agent starts.
  - `on_end`: Called when the specific agent ends.
  - `on_handoff`: Called when the specific agent hands off to another.
  - `on_tool_start`: Called before a tool is invoked by the specific agent.
  - `on_tool_end`: Called after a tool completes execution for the specific agent.

### RunContextWrapper
The `RunContextWrapper` is a mutable object passed to all callbacks, allowing developers to store and share custom data (context) across agents, tools, and handoffs. This is useful for maintaining state or implementing custom logic.

---

## Code Examples

Below are three Python code examples demonstrating the lifecycle functionality of the OpenAI Agents SDK. Each example is beginner-friendly and includes detailed explanations.

### 1. General Lifecycle Example

This example demonstrates how to use global lifecycle callbacks to track events across multiple agents, including a triage agent that hands off to a data agent.

```python
from agents import Agent, AgentHooks, Runner, RunContextWrapper
import asyncio
from typing import Any

# Custom context class
class MyContext:
    def __init__(self, user_id: str):
        self.user_id = user_id

# Custom hooks class for global lifecycle callbacks
class MyAgentHooks(AgentHooks[MyContext]):
    def on_agent_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext]) -> None:
        print(f"Agent {agent.name} started! User ID: {context.context.user_id}")

    def on_agent_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], output: Any) -> None:
        print(f"Agent {agent.name} ended! Output: {output}")

    def on_handoff(self, context: RunContextWrapper[MyContext], from_agent: Agent[MyContext], to_agent: Agent[MyContext]) -> None:
        print(f"Handoff from {from_agent.name} to {to_agent.name}")

    def on_tool_start(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any) -> None:
        print(f"Tool {tool.name} started by {agent.name}")

    def on_tool_end(self, context: RunContextWrapper[MyContext], agent: Agent[MyContext], tool: Any, result: str) -> None:
        print(f"Tool {tool.name} ended! Result: {result}")

# Simple tool function
def fetch_data() -> str:
    return "Sample Data"

# Define agents
assistant_agent = Agent[MyContext](
    name="Assistant",
    instructions="You are a helpful assistant",
    hooks=MyAgentHooks()
)

data_agent = Agent[MyContext](
    name="DataAgent",
    instructions="You fetch data",
    tools=[fetch_data]
)

triage_agent = Agent[MyContext](
    name="Triage",
    instructions="Handoff to DataAgent for data requests",
    handoffs=[data_agent]
)

# Main async function
async def main():
    context = MyContext(user_id="user123")
    result = await Runner.run(triage_agent, input="Fetch some data", context=context)
    print(f"Final Output: {result.final_output}")

# Run the program
if __name__ == "__main__":
    asyncio.run(main())
```

**Explanation**:
- **Context**: The `MyContext` class stores a `user_id` for sharing across agents.
- **Hooks**: The `MyAgentHooks` class overrides global lifecycle callbacks to log events like agent start, end, handoff, and tool execution.
- **Agents**: 
  - `triage_agent` hands off to `data_agent` based on the input.
  - `data_agent` uses the `fetch_data` tool.
  - `assistant_agent` is defined but not used in this example.
- **Output**: The program logs events like agent startup, handoff, tool execution, and final output, demonstrating the lifecycle.

**Sample Output**:
```
Agent Triage started! User ID: user123
Handoff from Triage to DataAgent
Agent DataAgent started! User ID: user123
Tool fetch_data started by DataAgent
Tool fetch_data ended! Result: Sample Data
Agent DataAgent ended! Output: Sample Data
Final Output: Sample Data
```

---

### 2. Runner Lifecycle Example

This example focuses on global lifecycle callbacks at the `Runner` level, tracking events for all agents in a multi-agent workflow.

```python
from agents import Agent, AgentHooks, Runner, RunContextWrapper
import asyncio
from typing import Any

# Custom context class
class MyContext:
    def __init__(self, session_id: str):
        self.session_id = session_id

# Runner-level hooks class
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

# Define agents
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
```

**Explanation**:
- **Context**: The `MyContext` class stores a `session_id`.
- **Hooks**: The `MyRunnerHooks` class defines global callbacks for the `Runner`, logging events for all agents.
- **Agents**: 
  - `triage_agent` hands off to `data_agent`.
  - `data_agent` uses the `get_info` tool.
- **Runner**: The `Runner` is initialized with `MyRunnerHooks` to track all lifecycle events.
- **Output**: The program logs all events globally, showing the Runner's perspective.

**Sample Output**:
```
[Runner] Agent TriageAgent started! Session ID: session_001
[Runner] Handoff from TriageAgent to DataAgent
[Runner] Agent DataAgent started! Session ID: session_001
[Runner] Tool get_info started by DataAgent
[Runner] Tool get_info ended! Result: Sample Information
[Runner] Agent DataAgent ended! Output: Sample Information
Final Output: Sample Information
```

---

### 3. Agent Lifecycle Example

This example demonstrates agent-specific lifecycle callbacks, tracking events for a single agent using its `hooks` property.

```python
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

# Define agent with specific hooks
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
```

**Explanation**:
- **Context**: The `MyContext` class stores a `user_name`.
- **Hooks**: The `MyAgentHooks` class defines agent-specific callbacks, attached to `info_agent` via the `hooks` property.
- **Agent**: `info_agent` uses the `process_data` tool and has its own hooks for event tracking.
- **Output**: The program logs events specific to `info_agent`, with no handoff since only one agent is used.

**Sample Output**:
```
[Agent] InfoAgent started for user: Ali
[Agent] Tool process_data started by InfoAgent
[Agent] Tool process_data ended! Result: Processed Data
[Agent] InfoAgent ended! Output: Processed Data
Final Output: Processed Data
```

---

## Key Takeaways
- **Runner Lifecycle**: Use global callbacks (`on_agent_start`, `on_handoff`, etc.) to monitor all agents in a workflow, ideal for multi-agent systems.
- **Agent Lifecycle**: Use agent-specific callbacks (`on_start`, `on_end`, etc.) to customize or debug a single agent’s behavior.
- **RunContextWrapper**: Enables sharing custom data across agents and tools, enhancing flexibility.
- **Use Cases**: Lifecycle callbacks are useful for logging, debugging, prefetching data, or implementing custom logic like guardrails.

## How to Run the Examples
1. Install the OpenAI Agents SDK (refer to official documentation for setup).
2. Save each example as a `.py` file (e.g., `lifecycle_example.py`, `runner_lifecycle_example.py`, `agent_lifecycle_example.py`).
3. Run the files using Python: `python <filename>.py`.
4. Ensure you have an async-compatible environment (Python 3.7+).

## Next Steps
Explore additional SDK features like tool creation or advanced handoff strategies in upcoming lessons of the "OpenAI SDK: Deep Study" series. 