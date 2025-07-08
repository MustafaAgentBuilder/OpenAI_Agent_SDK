from agents import Agent , Runner , function_tool , handoffs , set_tracing_disabled
from openai.types.responses.easy_input_message_param import EasyInputMessageParam
from openai.types.responses.response_input_text_param import ResponseInputTextParam
from openai.types.responses.response_input_image_param import ResponseInputImageParam
from openai.types.responses.response_input_item_param import Message
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import asyncio
load_dotenv()
set_tracing_disabled(True)


import os

# Retrieve the actual API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

model = LitellmModel(
    api_key=groq_api_key,
    model="groq/gemma2-9b-it"
)



@function_tool(name_override="Weather Tool")
async def weather():
    """
    Dummy weather function that returns a simple weather report.
    Returns:
        str: A dummy weather report indicating if it's sunny or rainy.
    """
    import random

    weather_conditions = ["The weather is sunny.", "The weather is rainy."]
    return random.choice(weather_conditions)

city_agent = Agent(
    name="city_agent",
    instructions=(
        "You are the City agent. When the triage agent hands off a request about the weather in a city, "
        "use the weather tool to provide the current weather information for the specified city."
    ),
    tools=[weather],
    model=model
)



triage_Agent = Agent(
    name="triage_Agent",
    instructions=(
        "You are a helpful assistant. "
        "If the user asks about the weather in any city, hand off the request to the City agent. "
        "Otherwise, assist the user with their queries."
    ),
    model=model,
    handoffs=[city_agent]
)


"""
# Note: The following code structure is intended for development and testing purposes only.
# Running asynchronous event loops directly (e.g., with asyncio.run) and using input() for user interaction
# is not recommended in production environments, as it may lead to unexpected crashes or unhandled exceptions.
# For production, consider implementing robust error handling, logging, and a proper interface (such as a web API).
"""
async def demo() -> None:
    """
    Runs a demo loop where the user can interact with the triage agent.
    The loop continues until the user enters 'exit' or 'quit'.
    """
    while True:
        user_input = input("Enter your query (or type 'exit' to quit): ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting demo loop.")
            break
        response = await Runner.run(
            starting_agent=triage_Agent,
            input=user_input
        )
        print("Agent response:", response)


if __name__ == "__main__":
    asyncio.run(demo())



async def demo1() -> None:
    """
    Production-Ready Runner Loop

    This function demonstrates a robust pattern for running an agent loop in production environments.
    Instead of passing a simple string to Runner.run, it constructs a structured input using
    EasyInputMessageParam and ResponseInputTextParam. This approach is more reliable and extensible,
    allowing for richer message types, roles, and content, which is essential for complex agent workflows.

    Key Features:
    - Accepts user input interactively.
    - Exits cleanly on 'exit' or 'quit'.
    - Wraps user input in a structured message format for the agent.
    - Awaits the agent's response and prints it.

    This method is preferred over simple string-based Runner.run calls in production, as it
    supports advanced input handling and better aligns with agent communication protocols.
    """

    while True:
        user_input = input("Enter your query (or type 'exit' to quit): ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting demo loop.")
            break

        # Construct a structured input message for the agent
        input_message = EasyInputMessageParam(
            role="user",
            type="message",
            content=[
                ResponseInputTextParam(
                    text=user_input,
                    type="input_text"
                )
            ]
        )

        response = await Runner.run(
            starting_agent=triage_Agent,
            input=[input_message]
        )

        print("Agent response:", response.final_output)
        


# # To run the demo loop, uncomment the following lines:
if __name__ == "__main__":
    asyncio.run(demo1())





"""
About EasyInputMessageParam and Its Advantages

The use of `EasyInputMessageParam` (or similarly structured message classes) is a significant improvement over passing simple strings to agent runners. This approach provides a robust, extensible, and semantically rich way to communicate with agents, especially in complex multi-agent or tool-using workflows.

**Why is this better?**

1. **Structured Communication:**  
   By wrapping user input in a message object with explicit fields for `role`, `type`, and `content`, we ensure that the agent receives all necessary context. This structure is essential for advanced agent orchestration, where different message types (e.g., user, system, tool) may be handled differently.

2. **Extensibility:**  
   As agent capabilities grow, you may want to include additional metadata, attachments, or message types. Structured input makes it easy to extend the protocol without breaking existing functionality.

3. **Reliability:**  
   Structured messages reduce ambiguity and parsing errors. The agent can reliably extract the user's intent and any additional parameters, leading to more accurate and predictable responses.

4. **Alignment with Agent Protocols:**  
   Modern agent frameworks (like OpenAI Agents SDK, CrewAI, LangGraph) expect messages in a structured format. Using `EasyInputMessageParam` ensures compatibility and leverages the full power of these frameworks.

5. **Final Input Stage:**  
   This is the last stage before the agent processes the input. Here, you have the opportunity to validate, enrich, or transform the user's input as needed, ensuring that the agent receives exactly what it needs to perform optimally.

**Summary:**  
Using structured input messages like `EasyInputMessageParam`or `Message` is a best practice for building scalable, maintainable, and future-proof agent applications. It enables richer interactions, better error handling, and seamless integration with advanced agent features.

"""




async def demo2():
    while True:
        user_input = input("Enter your query (or type 'exit' to quit): ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting demo loop.")
            break

        # Construct a structured input message for the agent
        input_message = Message(
            role="user",
            type="message",
            content=[
                ResponseInputTextParam(
                    text=user_input,
                    type="input_text"
                )
            ]
        )

        response = await Runner.run(
            starting_agent=triage_Agent,
            input=[input_message]
        )

        print("Agent response:", response.final_output)


if __name__ == "__main__":
    asyncio.run(demo2())


