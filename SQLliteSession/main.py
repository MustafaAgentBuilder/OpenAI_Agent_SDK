from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled , SQLiteSession
from dotenv import load_dotenv 
from openai import AsyncOpenAI 
from agents.items import TResponseInputItem
from typing import Protocol, List, Optional
import asyncio
import os
import asyncio

# Load environment variables from a .env file
load_dotenv()

# Disable extra tracing/logging for cleaner output
set_tracing_disabled(True)

# This code is written by me to use this open-source SDK

# Create an API provider with AsyncOpenAI using your API key and base URL.
Provider = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completion model with the API provider.
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)


# ─── Your Session & Agent Setup ────────────────────────────────────────────────

# Create or open the SQLite-backed session store
session = SQLiteSession("user_2", "conversation.db")

# Define your greeting agent
GreetingAgent = Agent(
    name="Greeting Agent",
    instructions="You greet the user and assist with their queries.",
    model=model  # or whatever model variable you have
)

# Run the agent once to store the first message
response = Runner.run_sync(
    GreetingAgent,
    "My name is Mustafa and my age is 18",
    session=session
)
print("Bot:", response.final_output)

# ─── Session Protocol Definition ────────────────────────────────────────────────

class Session(Protocol):
    """Protocol for session implementations."""

    session_id: str

    async def get_items(self, limit: Optional[int] = None) -> List[TResponseInputItem]:
        """Retrieve up to `limit` items (or all if None)."""
        ...

    async def add_items(self, items: List[TResponseInputItem]) -> None:
        """Add new items to the session history."""
        ...

    async def pop_item(self) -> Optional[TResponseInputItem]:
        """Remove and return the most recent item, or None if empty."""
        ...

    async def clear_session(self) -> None:
        """Delete all items in this session."""
        ...

# ─── (Optional) Example: Using the Protocol Asynchronously ───────────────────────

# If you ever need to call those async methods, wrap them like this:
# 3️⃣ Helper to call async methods
def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

# 4️⃣ Fetch & print history correctly (dict access)
all_history = run_async(session.get_items(limit=1))
print("\nConversation history:")
for item in all_history:
    print(f"{item['role']}: {item['content']}")

# 5️⃣ Clear session if you like
run_async(session.clear_session())
print("\nSession cleared.")