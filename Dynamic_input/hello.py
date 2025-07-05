# Two main Thing to Note:
# 1. Dynamic input function is not run asynchronously, but synchronously.
# 2. If we want to run it asynchronously, we can use `await Runner.run(...) or add await in input parameter.`




from agents import Agent , Runner , RunContextWrapper , OpenAIChatCompletionsModel , set_tracing_disabled , TContext

from openai import AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv 
import os
import asyncio


# Load environment variables from a .env file
load_dotenv()

# Disable extra tracing/logging for cleaner output
set_tracing_disabled(True)

# This code is written by me to use this open-source SDK

# Create an API provider with AsyncOpenAI using your API key and base URL.
Provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completion model with the API provider.
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=Provider,
)



from pydantic import BaseModel
from agents import RunContextWrapper, Agent, Runner

# 1. Define your data model with Pydantic
class UserInfo(BaseModel):
    name: str
    age: int
    city: str

# 2. Create an instance of your model
user = UserInfo(name="John", age=30, city="New York")



def my_tool(wrapper: RunContextWrapper, input: str):
    print("Total tokens used so far:", wrapper.usage.total_tokens)




# 3. Write with  async 
async def dynamic_input(
    input_str: str,
    wrapper: RunContextWrapper[UserInfo],
    agent: Agent[UserInfo],
) -> str:
    # Access the actual context object via wrapper.context
    info = f"{wrapper.context} | Agent name: {agent.name}"
    return f"{input_str} → {info}"

# 4. Create your agent
agent = Agent(
    model=model,
    name="Assistant",
    instructions="You are a helpful assistant.",
)

# 5. Run the agent synchronously
#    • Pass the coroutine dynamic_input(...) directly as the `input` argument.
#    • Fixed an extra comma and misplaced parentheses.

async def run_agent():
    response = await Runner.run(
        agent,
        input=await dynamic_input(
            "Hello, how can I assist you today?",
            wrapper=RunContextWrapper(context=user),
            agent=agent,
        ),
        context=user,
    )
    print response # type: ignore


# 6. Print out the whole response object and the final text
    print(response)
    print(response.final_output)


if __name__ == "__main__":
    # Run the async function using asyncio.run
    asyncio.run(run_agent())


#-------------------------------------------------------------------------------#-

# - Write with sync
def dynamic_input(
    input_str: str,
    wrapper: RunContextWrapper[UserInfo],
    agent: Agent[UserInfo],
) -> str:
    # Access the actual context object via wrapper.context
    info = f"{wrapper.context} | Agent name: {agent.name}"
    return f"{input_str} → {info}"

# 4. Create your agent
agent = Agent(
    model=model,
    name="Assistant",
    instructions="You are a helpful assistant.",
)




response = Runner.run_sync(
    agent,
    input= dynamic_input(
            "Hello, how can I assist you today?",
            wrapper=RunContextWrapper(context=user),
            agent=agent,
        ),
    context=user,
    )
print ("Sync Response:")
print(response)
print(response.final_output)