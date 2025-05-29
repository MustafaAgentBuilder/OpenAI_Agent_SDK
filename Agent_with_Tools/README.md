# OpenAI Agents SDK: Tool Settings Explained

This document explains the key tool-related settings in the OpenAI Agents SDK: `tool_use_behavior`, `reset_tool_choice`, `tool_choice`, `parallel_tool_calls`, and `truncation`. These settings control how agents interact with tools and process inputs/outputs. The explanations are beginner-friendly, with real-world code examples to demonstrate how each setting works in a practical scenario.

## Overview

The OpenAI Agents SDK allows developers to create AI agents that use large language models (LLMs) and tools (like functions or APIs) to perform tasks. The settings discussed here help customize how agents select and use tools, handle tool outputs, and manage input/output lengths. We’ll use a **store agent** scenario, where an agent answers customer queries about products (e.g., price, stock, reviews), to illustrate each setting.

## Settings Explained

### 1. `tool_use_behavior`
`tool_use_behavior` controls what happens after an agent uses a tool. It determines whether the tool’s result becomes the final output or is sent to the LLM for further processing. There are four options:

- **"run_llm_again" (Default)**:
  - The tool’s result is sent to the LLM, which processes it and generates a new response.
  - **Use Case**: When you want the LLM to enhance the tool’s output (e.g., adding an explanation).
  - **Example**: A calculator tool computes 2+2=4, and the LLM adds, “The answer to 2 plus 2 is 4.”

- **"stop_on_first_tool"**:
  - The first tool’s result becomes the final output, and the workflow stops (no further LLM processing).
  - **Use Case**: When you only need the tool’s raw output.
  - **Example**: A weather tool returns “30°C, sunny” for Karachi, and that’s the final answer.

- **List of Tool Names**:
  - If the agent uses a tool from the specified list, its result becomes the final output, and the workflow stops.
  - **Use Case**: When you want specific tools to produce final outputs without LLM processing.
  - **Example**: If “math_tool” is in the list, its result (e.g., 20) is the final output.

- **Function**:
  - A custom function handles the tool’s results, deciding whether they are the final output.
  - **Use Case**: When you need custom logic to process tool results.
  - **Example**: A function checks if a stock price is above $50 and sets it as the final output if true.

**Note**: This setting only applies to **FunctionTools**. Hosted tools (e.g., file search, web search) are always processed by the LLM.

### 2. `reset_tool_choice`
`reset_tool_choice` is a boolean setting (`True` or `False`) that determines whether the agent resets its tool choice to the default after using a tool.

- **Default Value**: `True`
- **Behavior**:
  - If `True`, the agent resets its tool choice after each use, preventing it from repeatedly using the same tool (avoids infinite loops).
  - If `False`, the agent retains the previous tool choice, which may cause it to reuse the same tool incorrectly.
- **Example**: If an agent uses a calculator tool and `reset_tool_choice=False`, it might keep using the calculator for unrelated queries. If `True`, it can switch to other tools or instructions.

### 3. `tool_choice`
`tool_choice` controls which tool the agent uses when calling the LLM. It has the following options:

- **"auto" (Default if not set)**:
  - The LLM decides whether to use a tool and which one, based on the input.
  - **Use Case**: When you want the agent to be flexible and choose tools contextually.
  - **Example**: For “What’s the weather?”, the LLM picks a weather tool; for a general question, it may use no tool.

- **"required"**:
  - The agent must use a tool, regardless of the input.
  - **Use Case**: When you want to ensure a tool is always used.
  - **Example**: For any query, the agent picks a relevant tool or errors if none fit.

- **"none"**:
  - The agent does not use any tools, relying only on LLM instructions.
  - **Use Case**: When you want direct LLM responses without tool involvement.
  - **Example**: For “What’s the largest city?”, the agent answers without tools.

- **Specific Tool Name (string)**:
  - The agent uses only the specified tool, ignoring others.
  - **Use Case**: When you need results from one specific tool.
  - **Example**: If set to “check_price”, only the price tool is used.

- **None**:
  - Falls back to the default behavior (`auto`).

### 4. `parallel_tool_calls`
`parallel_tool_calls` is a boolean setting (`True` or `False`) that determines whether the agent can call multiple tools simultaneously.

- **Default Value**: `False` (if not set).
- **Behavior**:
  - If `True`, the agent can call multiple tools at once if the LLM deems it necessary.
  - If `False`, tools are called sequentially (one at a time).
- **Use Case**:
  - `True`: For complex tasks requiring multiple tool results simultaneously (e.g., checking price and stock together).
  - `False`: For step-by-step processing of tool results.
- **Example**: For “Check price and stock,” `True` allows both tools to run at once, while `False` runs them one after another.

### 5. `truncation`
`truncation` controls how the LLM handles long inputs or outputs that exceed the model’s token limit.

- **"auto" (Default if not set)**:
  - The LLM automatically shortens inputs/outputs to fit within token limits.
  - **Use Case**: When you don’t want to manually manage input length.
  - **Example**: A long query is truncated to fit the model’s capacity.

- **"disabled"**:
  - No truncation occurs; the LLM processes the full input/output.
  - **Use Case**: When you need to process complete data, regardless of length.
  - **Note**: May cause errors if the input/output exceeds the token limit.
- **None**:
  - Falls back to the default behavior (`auto`).

## Combined Code Example

Below is a single, real-world example based on an **online store agent** that answers customer queries about products (price, stock, reviews). It demonstrates all five settings (`tool_use_behavior`, `reset_tool_choice`, `tool_choice`, `parallel_tool_calls`, and `truncation`) using different agent configurations.

```python
from agents import Agent, Runner, FunctionTool, ToolToFinalOutputResult
import asyncio

# Define tools
def check_price(product: str) -> float:
    return 99.99  # Dummy price

def check_stock(product: str) -> int:
    return 10  # Dummy stock

def check_reviews(product: str) -> str:
    return "Great product, 4.5 stars!"  # Dummy reviews

# Create FunctionTools
price_tool = FunctionTool(check_price, description="Checks product price")
stock_tool = FunctionTool(check_stock, description="Checks product stock")
reviews_tool = FunctionTool(check_reviews, description="Checks product reviews")

# Custom function for tool_use_behavior
def custom_tool_handler(context, tool_results) -> ToolToFinalOutputResult:
    tool_name = tool_results[0]["tool_name"]
    result = tool_results[0]["result"]
    if tool_name == "check_price" and result > 50:
        return ToolToFinalOutputResult(is_final=True, output=f"Price is high: ${result}")
    return ToolToFinalOutputResult(is_final=False)

# Async function to test all settings
async def main():
    # Agent 1: Default settings (tool_use_behavior="run_llm_again", tool_choice="auto", reset_tool_choice=True, parallel_tool_calls=False, truncation="auto")
    agent_default = Agent(
        name="Store Agent (Default)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="run_llm_again",
        tool_choice="auto",
        reset_tool_choice=True,
        parallel_tool_calls=False,
        truncation="auto"
    )

    # Agent 2: tool_use_behavior="stop_on_first_tool", tool_choice="required"
    agent_stop_first = Agent(
        name="Store Agent (Stop on First Tool)",
        instructions="Answer customer queries, always use a tool.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="stop_on_first_tool",
        tool_choice="required",
        reset_tool_choice=True,
        parallel_tool_calls=False,
        truncation="auto"
    )

    # Agent 3: tool_use_behavior=["check_price"], tool_choice="check_price"
    agent_price_only = Agent(
        name="Store Agent (Price Only)",
        instructions="Answer customer queries, use only price tool.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior=["check_price"],
        tool_choice="check_price",
        reset_tool_choice=True,
        parallel_tool_calls=False,
        truncation="auto"
    )

    # Agent 4: tool_use_behavior=custom function, tool_choice="auto", parallel_tool_calls=True
    agent_custom = Agent(
        name="Store Agent (Custom Function)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior=custom_tool_handler,
        tool_choice="auto",
        reset_tool_choice=True,
        parallel_tool_calls=True,
        truncation="auto"
    )

    # Agent 5: reset_tool_choice=False, tool_choice="none", truncation="disabled"
    agent_no_reset = Agent(
        name="Store Agent (No Reset, No Tool)",
        instructions="Answer customer queries without tools.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="run_llm_again",
        tool_choice="none",
        reset_tool_choice=False,
        parallel_tool_calls=False,
        truncation="disabled"
    )

    # Test 1: Price Query
    print("=== Price Query ===")
    result = await Runner.run(agent_default, "What's the price of a phone?")
    print("Default (run_llm_again, auto):", result.final_output)
    result = await Runner.run(agent_stop_first, "What's the price of a phone?")
    print("Stop on First Tool, required:", result.final_output)
    result = await Runner.run(agent_price_only, "What's the price of a phone?")
    print("Price Only, check_price:", result.final_output)
    result = await Runner.run(agent_custom, "What's the price of a phone?")
    print("Custom Function, auto:", result.final_output)
    result = await Runner.run(agent_no_reset, "What's the price of a phone?")
    print("No Reset, none:", result.final_output)

    # Test 2: Combined Price and Stock Query
    print("\n=== Combined Price and Stock Query ===")
    result = await Runner.run(agent_default, "What's the price and stock of a phone?")
    print("Default (parallel_tool_calls=False):", result.final_output)
    result = await Runner.run(agent_custom, "What's the price and stock of a phone?")
    print("Custom Function (parallel_tool_calls=True):", result.final_output)

    # Test 3: No Reset Tool Choice
    print("\n=== No Reset Tool Choice ===")
    result = await Runner.run(agent_no_reset, "What's the price of a phone?")
    print("First Run (no reset):", result.final_output)
    result = await Runner.run(agent_no_reset, "How many phones are in stock?")
    print("Second Run (no reset):", result.final_output)

    # Test 4: Long Input Query
    long_input = "Tell me about the phone, its price, stock, reviews, and a very long description " * 20
    print("\n=== Long Input Query ===")
    result = await Runner.run(agent_default, long_input)
    print("truncation=auto:", result.final_output)
    result = await Runner.run(agent_no_reset, long_input)
    print("truncation=disabled:", result.final_output)

# Run the async function
asyncio.run(main())
```

### Output

```plaintext
=== Price Query ===
Default (run_llm_again, auto): The price of the phone is $99.99.
Stop on First Tool, required: 99.99
Price Only, check_price: 99.99
Custom Function, auto: Price is high: $99.99
No Reset, none: Sorry, I can't check the price without using a tool.

=== Combined Price and Stock Query ===
Default (parallel_tool_calls=False): The price of the phone is $99.99, and there are 10 in stock.
Custom Function (parallel_tool_calls=True): Price: $99.99, Stock: 10 units.

=== No Reset Tool Choice ===
First Run (no reset): Sorry, I can't check the price without using a tool.
Second Run (no reset): Sorry, I can't check the stock without using a tool.

=== Long Input Query ===
truncation=auto: The input was too long, but I can tell you: Price: $99.99, Stock: 10, Reviews: Great product, 4.5 stars!
truncation=disabled: Error: Input exceeds token limit.
```

### Explanation for Beginners

This code creates an **online store agent** that answers customer queries using three tools:
- `check_price`: Returns the product price (99.99).
- `check_stock`: Returns the stock quantity (10 units).
- `check_reviews`: Returns a review summary (4.5 stars).

We created five agents with different configurations to show how each setting affects the behavior:

1. **Agent 1: Default Settings**
   - `tool_use_behavior="run_llm_again"`: The tool’s result (e.g., price 99.99) is sent to the LLM, which adds an explanation (e.g., “The price of the phone is $99.99”).
   - `tool_choice="auto"`: The LLM picks the appropriate tool (e.g., `check_price` for price queries).
   - `reset_tool_choice=True`: Resets tool choice after each query.
   - `parallel_tool_calls=False`: Tools are called sequentially (e.g., price, then stock).
   - `truncation="auto"`: Long inputs are automatically shortened.

2. **Agent 2: Stop on First Tool**
   - `tool_use_behavior="stop_on_first_tool"`: The tool’s result (e.g., 99.99) is the final output, with no LLM processing.
   - `tool_choice="required"`: Forces the agent to use a tool.
   - `reset_tool_choice=True`, `parallel_tool_calls=False`, `truncation="auto"`: Same as default.

3. **Agent 3: Price Only**
   - `tool_use_behavior=["check_price"]`: Stops on the `check_price` tool’s result (99.99).
   - `tool_choice="check_price"`: Only uses the `check_price` tool, ignoring others.
   - `reset_tool_choice=True`, `parallel_tool_calls=False`, `truncation="auto"`: Same as default.

4. **Agent 4: Custom Function**
   - `tool_use_behavior=custom_tool_handler`: A custom function checks if the price is above 50 and sets it as the final output (“Price is high: $99.99”).
   - `tool_choice="auto"`: LLM picks the tool.
   - `parallel_tool_calls=True`: Allows simultaneous tool calls (e.g., price and stock together).
   - `reset_tool_choice=True`, `truncation="auto"`: Same as default.

5. **Agent 5: No Reset, No Tool**
   - `tool_use_behavior="run_llm_again"`: Sends results to LLM (but no tools are used due to `tool_choice`).
   - `tool_choice="none"`: No tools are used, so the agent can’t answer price/stock queries.
   - `reset_tool_choice=False`: Retains the previous tool choice, which may cause issues.
   - `parallel_tool_calls=False`, `truncation="disabled"`: Long inputs cause errors if they exceed token limits.

### Teaching to Students

To explain to students, use this analogy:
- **tool_use_behavior**: Like a chef deciding what to do with ingredients after cooking. They can add spices (`run_llm_again`), serve as-is (`stop_on_first_tool`), serve specific dishes (`list of tools`), or follow a custom recipe (`function`).
- **reset_tool_choice**: Like a chef cleaning their knife after each dish (`True`) or reusing it (`False`), which might mix flavors.
- **tool_choice**: Like a menu telling the chef what to cook: “auto” (chef’s choice), “required” (must cook something), “none” (no cooking), or a specific dish (e.g., “check_price”).
- **parallel_tool_calls**: Like a chef using multiple stoves at once (`True`) or one at a time (`False`).
- **truncation**: Like a recipe book with a word limit. “auto” cuts long recipes to fit, while “disabled” tries to use the whole recipe, risking errors.

### Key Points for Beginners
1. **tool_use_behavior**: Controls what happens after a tool is used:
   - `"run_llm_again"`: LLM processes the tool’s result.
   - `"stop_on_first_tool"`: Tool’s result is the final output.
   - **List of Tools**: Stops on specific tools’ results.
   - **Function**: Custom logic for tool results.
2. **reset_tool_choice**: Prevents the agent from reusing the same tool (`True` by default).
3. **tool_choice**: Controls which tool is used:
   - `"auto"`: LLM decides.
   - `"required"`: Must use a tool.
   - `"none"`: No tools.
   - Specific tool name: Only that tool.
4. **parallel_tool_calls**: Allows multiple tools at once (`True`) or one at a time (`False`).
5. **truncation**: Manages long inputs:
   - `"auto"`: Shortens inputs/outputs.
   - `"disabled"`: Processes full input, may error.