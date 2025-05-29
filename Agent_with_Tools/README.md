# OpenAI Agents SDK: `tool_use_behavior` and `reset_tool_choice` Explained

This document explains the `tool_use_behavior` and `reset_tool_choice` settings in the OpenAI Agents SDK in a beginner-friendly way, with real-world code examples to demonstrate how they work.

## What is `tool_use_behavior`?

`tool_use_behavior` is a setting that controls what happens after an agent uses a tool (like a function or API). It decides how the tool's result is handled and how the agent's workflow proceeds. There are four possible options:

1. **"run_llm_again" (Default Option)**:
   - When the agent uses a tool, the tool's result is sent to the LLM (language model).
   - The LLM reviews the result and generates a new response.
   - Use this when you want the LLM to further process or enhance the tool's output.
   - **Example**: If you use a calculator tool to compute 2+2, the result (4) goes to the LLM, which might add something like, "The answer to 2 plus 2 is 4."

2. **"stop_on_first_tool"**:
   - When the agent uses the first tool, its result becomes the final output.
   - The LLM does not process the result further, so the workflow stops.
   - Use this when you only need the tool's result without additional LLM processing.
   - **Example**: If you use a weather tool to check "Karachi's weather," the tool's output (e.g., "30°C, sunny") is the final answer.

3. **List of Tool Names**:
   - You can provide a list of specific tool names.
   - If the agent uses any tool from this list, its result becomes the final output, and the workflow stops.
   - The LLM does not process the result further.
   - **Example**: If you specify "weather_tool" or "math_tool" in the list, the agent stops after using these tools, and their output is the final answer.

4. **Function**:
   - You can provide a custom function to handle the tool's results.
   - This function takes the run context and tool results as input and returns a `ToolToFinalOutputResult`, which decides if the tool's result is the final output.
   - Use this when you need precise control over what happens after a tool is used.
   - **Example**: You can create a function that checks if a tool's result is valid and decides whether to stop or continue the workflow.

**Note**: These settings only apply to **FunctionTools**. Hosted tools (like file search or web search) are always processed by the LLM, so these settings do not affect them.

## What is `reset_tool_choice`?

`reset_tool_choice` is a boolean setting (True or False) that determines whether the agent's tool choice is reset to its default value after a tool is used.

- **Default Value**: `True`
- **Meaning**: When `True`, the agent resets its tool choice after using a tool. This prevents the agent from repeatedly using the same tool and getting stuck in an infinite loop.
- **If False**: The agent keeps the same tool choice it used previously, which might cause it to loop on the same tool.
- **Example**: If an agent uses a calculator tool and `reset_tool_choice=False`, it might keep using the calculator repeatedly. If `True`, it can switch to other tools or instructions.

## Code Examples

Below are beginner-friendly code examples that demonstrate each `tool_use_behavior` option and `reset_tool_choice` in real-world scenarios.

### Example 1: `tool_use_behavior = "run_llm_again"`

This example creates an agent that uses a math tool and processes its result with the LLM.

```python
from agents import Agent, Runner, FunctionTool
import asyncio

# Define a simple math tool
def add_numbers(a: int, b: int) -> int:
    return a + b

# Create a FunctionTool
math_tool = FunctionTool(add_numbers, description="Adds two numbers")

# Create an agent with run_llm_again behavior
agent = Agent(
    name="Math Agent",
    instructions="Use the math tool to add numbers and explain the result.",
    tools=[math_tool],
    tool_use_behavior="run_llm_again"
)

# Async function to run the agent
async def main():
    result = await Runner.run(agent, "Add 5 and 3, then explain the result.")
    print(result.final_output)

# Run the async function
asyncio.run(main())
```

**Output**:
```
The sum of 5 and 3 is 8. This was calculated using the math tool.
```

**Explanation**:
- The `math_tool` adds 5 and 3 (result: 8).
- Because `tool_use_behavior="run_llm_again"`, the result (8) is sent to the LLM, which returns it with an explanation.
- This is the default behavior, where the LLM enhances the tool's result.

### Example 2: `tool_use_behavior = "stop_on_first_tool"`

This example creates an agent that uses a weather tool, and the tool's result is the final output.

```python
from agents import Agent, Runner, FunctionTool
import asyncio

# Define a weather tool
def get_weather(city: str) -> str:
    return f"Weather in {city} is 30°C, sunny."

# Create a FunctionTool
weather_tool = FunctionTool(get_weather, description="Gets weather for a city")

# Create an agent with stop_on_first_tool behavior
agent = Agent(
    name="Weather Agent",
    instructions="Get the weather for a city.",
    tools=[weather_tool],
    tool_use_behavior="stop_on_first_tool"
)

# Async function to run the agent
async def main():
    result = await Runner.run(agent, "What's the weather in Karachi?")
    print(result.final_output)

# Run the async function
asyncio.run(main())
```

**Output**:
```
Weather in Karachi is 30°C, sunny.
```

**Explanation**:
- The `weather_tool` returns Karachi's weather.
- Because `tool_use_behavior="stop_on_first_tool"`, the tool's result (weather info) is the final output, and the LLM does not process it further.

### Example 3: `tool_use_behavior = List of Tool Names`

This example creates an agent with two tools and stops on a specific tool's result.

```python
from agents import Agent, Runner, FunctionTool
import asyncio

# Define two tools
def add_numbers(a: int, b: int) -> int:
    return a + b

def multiply_numbers(a: int, b: int) -> int:
    return a * b

# Create FunctionTools
add_tool = FunctionTool(add_numbers, description="Adds two numbers")
multiply_tool = FunctionTool(multiply_numbers, description="Multiplies two numbers")

# Create an agent that stops on multiply_tool
agent = Agent(
    name="Math Agent",
    instructions="Perform math operations.",
    tools=[add_tool, multiply_tool],
    tool_use_behavior=["multiply_numbers"]
)

# Async function to run the agent
async def main():
    result = await Runner.run(agent, "Multiply 4 and 5.")
    print(result.final_output)

# Run the async function
asyncio.run(main())
```

**Output**:
```
20
```

**Explanation**:
- The agent uses the `multiply_numbers` tool (4 * 5 = 20).
- Because `tool_use_behavior=["multiply_numbers"]`, when the `multiply_numbers` tool is called, its result (20) becomes the final output, and the LLM does not process it further.

### Example 4: `tool_use_behavior = Function`

This example uses a custom function to handle tool results.

```python
from agents import Agent, Runner, FunctionTool, ToolToFinalOutputResult
import asyncio

# Define a tool
def get_stock_price(symbol: str) -> float:
    return 100.0  # Dummy stock price

# Create a FunctionTool
stock_tool = FunctionTool(get_stock_price, description="Gets stock price")

# Custom function for tool_use_behavior
def custom_tool_handler(context, tool_results) -> ToolToFinalOutputResult:
    price = tool_results[0]["result"]
    if price > 50:
        return ToolToFinalOutputResult(is_final=True, output=f"Stock price is high: ${price}")
    return ToolToFinalOutputResult(is_final=False)

# Create an agent with a custom function
agent = Agent(
    name="Stock Agent",
    instructions="Check stock prices.",
    tools=[stock_tool],
    tool_use_behavior=custom_tool_handler
)

# Async function to run the agent
async def main():
    result = await Runner.run(agent, "Get the stock price for AAPL.")
    print(result.final_output)

# Run the async function
asyncio.run(main())
```

**Output**:
```
Stock price is high: $100.0
```

**Explanation**:
- The `stock_tool` returns a dummy stock price (100.0).
- The `custom_tool_handler` checks if the price is above 50. If so, it sets the final output and stops the workflow.
- This option is highly flexible when you need custom logic.

### Example 5: `reset_tool_choice`

This example shows how `reset_tool_choice` works.

```python
from agents import Agent, Runner, FunctionTool
import asyncio

# Define a tool
def get_time() -> str:
    return "12:00 PM"

# Create a FunctionTool
time_tool = FunctionTool(get_time, description="Gets current time")

# Create an agent with reset_tool_choice=False
agent = Agent(
    name="Time Agent",
    instructions="Keep checking the time.",
    tools=[time_tool],
    reset_tool_choice=False
)

# Async function to run the agent
async def main():
    result = await Runner.run(agent, "What's the time?")
    print(result.final_output)
    # Run again to see if tool choice persists
    result = await Runner.run(agent, "What's the time again?")
    print(result.final_output)

# Run the async function
asyncio.run(main())
```

**Output**:
```
12:00 PM
12:00 PM
```

**Explanation**:
- Because `reset_tool_choice=False`, the agent uses the same `time_tool` for the second query without resetting the tool choice.
- If `reset_tool_choice=True`, the agent might reset its tool choice and show different behavior.

## Key Points for Beginners

1. **tool_use_behavior**: Determines what happens after a tool is used:
   - `"run_llm_again"`: Sends the tool's result to the LLM for further processing.
   - `"stop_on_first_tool"`: Uses the tool's result as the final output.
   - **List of Tools**: Stops on the result of specific tools.
   - **Function**: Uses a custom function for custom logic.
2. **reset_tool_choice**: Ensures the agent doesn’t reuse the same tool repeatedly (`True` by default).
3. **FunctionTools vs Hosted Tools**: These settings only apply to FunctionTools; hosted tools (like web search) are always processed by the LLM.