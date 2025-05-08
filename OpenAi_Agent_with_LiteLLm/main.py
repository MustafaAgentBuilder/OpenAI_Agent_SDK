import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# LiteLLMModel makes it easy: no need to import or use AsyncOpenAI or OpenAIChatCompletionsModel.
# Just write simple, synchronous Python code—LiteLLM handles the async calls and API complexity for you.
from agents import Runner, Agent, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os
from dotenv import load_dotenv

set_tracing_disabled(True)
load_dotenv()

api_key     = os.getenv("GEMINI_API_KEY")
model_name  = os.getenv("MODEL")  # e.g., "gemini-pro"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=LitellmModel(model=model_name, api_key=api_key)
)

response = Runner.run_sync(
    starting_agent=agent,
    input="Tell me about the Pakistan v India war."
)

print(response.final_output)

