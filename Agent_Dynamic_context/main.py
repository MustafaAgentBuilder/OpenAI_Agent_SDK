import os, asyncio
from dataclasses import dataclass
# Assuming 'agents' is the correct package structure based on imports
from agents import Agent, RunContextWrapper, Runner
# Assuming 'agents.extensions.models' is correct
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in your environment")

@dataclass
class UserDynamic:
    user_id: int
    user_name: str
    user_email: str

def dynamic_instructions(
    context: RunContextWrapper[UserDynamic],
    dy_agent: Agent[UserDynamic], # Note: dy_agent parameter is currently unused in this function
) -> str:
    fixed = """
You are a highly knowledgeable Python tutor.
• Always answer in a clear, step-by-step style.
• Ask clarifying questions if needed.
• Tailor examples to a beginner audience.
"""
    # Access the user data from the context wrapper
    dynamic = f"The user’s name is {context.context.user_name}.\n"
    return fixed + "\n" + dynamic

async def main():
    user_ctx = UserDynamic(1, "Mustafa", "mustafaadeel989@gmail.com")

    # Initialize the agent outside the loop
    agent = Agent[UserDynamic](
        name="AssistanceAgent",
        model=LitellmModel(model="gemini/gemini-1.5-flash-latest", api_key=API_KEY),
        instructions=dynamic_instructions,
    )

    print("Python Tutor Agent initialized. Type 'quit' or 's' to exit.")

    while True:
        # 1. Get user input inside the loop
        user_input = input("You: ")

        # 2. Check for the exit condition (using the user's input)
        if user_input.lower() in ["quit", "s"]:
            break # Exit the loop if user types 'quit' or 's'

        # 3. Run the agent with the user's input
        try:
            # The result of Runner.run will be stored in agent_output
            agent_output = await Runner.run(
                starting_agent=agent,
                input=user_input, # Use the user's input here
                context=user_ctx
            )

            # 4. Print the agent's response
            # The exact way to get the text content might depend on what Runner.run returns.
            # Often, it returns a result object that needs further processing (e.g., result.output or result.last_message.content).
            # For simplicity, let's print the result object itself, as your original code did with 'runner'.
            # You might need to adjust this line based on the actual structure returned by Runner.run.
            print("Agent says:", agent_output)

        except Exception as e:
            print(f"An error occurred during the agent run: {e}")
            # Decide if you want to break the loop on error or continue
            # break # Uncomment to break on error
            pass # Continue the loop despite the error

    print("Exiting chat.")

if __name__ == "__main__":
    # Ensure you have an event loop policy if running on specific platforms like Windows
    # See https://docs.python.org/3/library/asyncio-policy.html
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")