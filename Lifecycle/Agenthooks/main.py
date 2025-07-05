import os
import asyncio
from dataclasses import dataclass

from agents import Agent, Runner, RunContextWrapper
from agents.extensions.models.litellm_model import LitellmModel
from agents.lifecycle import AgentHooks
from dotenv import load_dotenv

# 0. Load your API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY in your environment")

# 1. Define your context dataclass
@dataclass
class UserDynamic:
    user_id: int
    user_name: str
    user_email: str

# 2. Write a hooks class with the CORRECT method signatures
class MyDebugHooks(AgentHooks[UserDynamic]):
    # on_agent_start only gets the context wrapper (no 'agent' parameter)
    async def on_agent_start(self, context: RunContextWrapper[UserDynamic], **kwargs):
        print("\n--- HOOK: on_agent_start ---")
        print(f"Agent '{self.agent.name}' is starting.")  
        print(f"  user_id in context: {context.context.user_id}")
        print("---------------------------")

    async def after_initial_message(self, context: RunContextWrapper[UserDynamic], message, **kwargs):
        print("\n--- HOOK: after_initial_message ---")
        print(f"Got initial message: '{message.content}'")
        print("---------------------------")

    async def before_tool_calling(self, context: RunContextWrapper[UserDynamic], tool_calls, **kwargs):
        print("\n--- HOOK: before_tool_calling ---")
        for tc in tool_calls:
            name = getattr(tc.function, "name", "<unnamed>")
            args = getattr(tc.function, "arguments", {})
            print(f"→ will call {name} with {args}")
        print("---------------------------")

    async def before_message_sending(self, context: RunContextWrapper[UserDynamic], message, **kwargs):
        print("\n--- HOOK: before_message_sending ---")
        print(f"About to send: '{message.content}'")
        print("---------------------------")

    async def on_agent_end(self, context: RunContextWrapper[UserDynamic], **kwargs):
        print("\n--- HOOK: on_agent_end ---")
        print(f"Agent '{self.agent.name}' finished.")
        print("---------------------------")

async def main():
    # 3. Create your context instance
    user_ctx = UserDynamic(
        user_id=1,
        user_name="Mustafa",
        user_email="mustafa@example.com"
    )

    # 4. Instantiate the agent *with* your hooks
    agent = Agent[UserDynamic](
        name="ChattyAgent",
        model=LitellmModel(model="gemini/gemini-1.5-flash-latest", api_key=API_KEY),
        instructions="You are a helpful assistant. Be brief and answer the user's question.",
        hooks=MyDebugHooks(),   # ← attach your hooks here!
    )

    print("Starting agent run with hooks…")

    # 5. Run the agent *and* pass in your context
    result = await Runner.run(
        starting_agent=agent,
        input="Tell me a fun fact about sloths.",
        context=user_ctx        # ← this makes context_wrapper non-None in your hooks
    )

    print("\n--- Agent run finished ---")
    print("Final result:", result)

if __name__ == "__main__":
    asyncio.run(main())
