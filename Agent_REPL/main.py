import asyncio
from agents import Agent, Runner, function_tool
from agents.types import ChatMessage

# Define a custom tool
@function_tool
def get_greeting(name: str) -> str:
    """Returns a personalized greeting."""
    return f"Hello, {name}! How can I assist you today?"

# Define the agent
agent = Agent(
    name="Greeter",
    instructions="You are a friendly assistant. Use the get_greeting tool when appropriate.",
    tools=[get_greeting],
    model="gpt-4o"
)

# Custom interactive loop
async def interactive_loop() -> None:
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = await Runner.run(
            agent=agent,
            messages=[ChatMessage(content=user_input, role="user")],
            stream=False
        )
        print(f"Assistant: {result.final_output}")

# Main function
async def main() -> None:
    await interactive_loop()

if __name__ == "__main__":
    asyncio.run(main())