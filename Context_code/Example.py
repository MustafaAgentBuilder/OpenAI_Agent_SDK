
from agents import Agent, Runner, FunctionTool
from dataclasses import dataclass
import asyncio
from typing import List

# Define a Purchase class for structured data
@dataclass
class Purchase:
    item: str
    price: float

# Define the Context class
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> List[Purchase]:
        # Dummy purchase history based on user ID
        if self.uid == "user123":
            return [Purchase(item="Phone", price=99.99), Purchase(item="Headphones", price=29.99)]
        return []

# Define tools
def check_price(product: str, context: UserContext) -> float:
    base_price = 99.99  # Dummy price
    if context.is_pro_user:
        return base_price * 0.9  # 10% discount for pro users
    return base_price

def fetch_user_purchases(context: UserContext) -> List[Purchase]:
    # Run the async fetch_purchases method
    return asyncio.run(context.fetch_purchases())

# Create FunctionTools
price_tool = FunctionTool(check_price, description="Checks product price with discount for pro users")
purchases_tool = FunctionTool(fetch_user_purchases, description="Fetches user's purchase history")

# Create an agent with UserContext
agent = Agent[UserContext](
    name="Store Agent",
    instructions="Answer customer queries using user context. Apply discounts for pro users and fetch purchase history when asked.",
    tools=[price_tool, purchases_tool],
    tool_use_behavior="run_llm_again",
    tool_choice="auto",
    reset_tool_choice=True,
    parallel_tool_calls=False,
    truncation="auto"
)

# Async function to test the agent with different contexts
async def main():
    # Context for a pro user
    pro_user_context = UserContext(uid="user123", is_pro_user=True)
    
    # Context for a non-pro user
    non_pro_user_context = UserContext(uid="user456", is_pro_user=False)

    # Test 1: Price query for pro user
    print("=== Price Query (Pro User) ===")
    result = await Runner.run(agent, "What's the price of a phone?", context=pro_user_context)
    print("Pro User:", result.final_output)

    # Test 2: Price query for non-pro user
    print("\n=== Price Query (Non-Pro User) ===")
    result = await Runner.run(agent, "What's the price of a phone?", context=non_pro_user_context)
    print("Non-Pro User:", result.final_output)

    # Test 3: Purchase history query
    print("\n=== Purchase History Query ===")
    result = await Runner.run(agent, "What are my past purchases?", context=pro_user_context)
    print("Pro User Purchases:", result.final_output)

# Run the async function
asyncio.run(main())
