from agent import Agent, Runner, FunctionTool, ToolToFinalOutputResult
import asyncio

# Tool 1: Check Price
def check_price(product: str) -> float:
    return 99.99  # Dummy price

# Tool 2: Check Stock
def check_stock(product: str) -> int:
    return 10  # Dummy stock

# Tool 3: Check Reviews
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

# Async function to test different tool_use_behavior options
async def main():
    # Agent 1: tool_use_behavior = "run_llm_again" (Default)
    agent_run_llm = Agent(
        name="Store Agent (Run LLM Again)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="run_llm_again",
        reset_tool_choice=True
    )

    # Agent 2: tool_use_behavior = "stop_on_first_tool"
    agent_stop_first = Agent(
        name="Store Agent (Stop on First Tool)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="stop_on_first_tool",
        reset_tool_choice=True
    )

    # Agent 3: tool_use_behavior = ["check_price"]
    agent_stop_price = Agent(
        name="Store Agent (Stop on Price Tool)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior=["check_price"],
        reset_tool_choice=True
    )

    # Agent 4: tool_use_behavior = custom function
    agent_custom = Agent(
        name="Store Agent (Custom Function)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior=custom_tool_handler,
        reset_tool_choice=True
    )

    # Agent 5: reset_tool_choice = False
    agent_no_reset = Agent(
        name="Store Agent (No Reset)",
        instructions="Answer customer queries about products.",
        tools=[price_tool, stock_tool, reviews_tool],
        tool_use_behavior="run_llm_again",
        reset_tool_choice=False
    )

    # Test 1: Price Query
    print("=== Price Query ===")
    result = await Runner.run(agent_run_llm, "What's the price of a phone?")
    print("Run LLM Again:", result.final_output)
    result = await Runner.run(agent_stop_first, "What's the price of a phone?")
    print("Stop on First Tool:", result.final_output)
    result = await Runner.run(agent_stop_price, "What's the price of a phone?")
    print("Stop on Price Tool:", result.final_output)
    result = await Runner.run(agent_custom, "What's the price of a phone?")
    print("Custom Function:", result.final_output)

    # Test 2: Stock Query
    print("\n=== Stock Query ===")
    result = await Runner.run(agent_run_llm, "How many phones are in stock?")
    print("Run LLM Again:", result.final_output)
    result = await Runner.run(agent_stop_first, "How many phones are in stock?")
    print("Stop on First Tool:", result.final_output)
    result = await Runner.run(agent_stop_price, "How many phones are in stock?")
    print("Stop on Price Tool:", result.final_output)
    result = await Runner.run(agent_custom, "How many phones are in stock?")
    print("Custom Function:", result.final_output)

    # Test 3: No Reset Tool Choice
    print("\n=== No Reset Tool Choice ===")
    result = await Runner.run(agent_no_reset, "What's the price of a phone?")
    print("First Run:", result.final_output)
    result = await Runner.run(agent_no_reset, "How many phones are in stock?")
    print("Second Run (No Reset):", result.final_output)

# Run the async function
asyncio.run(main())