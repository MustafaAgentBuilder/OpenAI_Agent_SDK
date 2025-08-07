import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, handoff, OpenAIChatCompletionsModel 
from tools import search_everything, fetch_latest_news

# Load .env and API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

# Set up the provider and model
provider = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-preview-04-17",
    openai_client=provider,
)

def create_assistant_agent() -> Agent:
    # Sub-agent for general web research
    google_agent = Agent(
        name="GoogleSearcher",
        instructions=(
            "You are GoogleSearcher, an AI specialized in finding reliable information online. "
            "When a user asks for definitions, explanations, or factual details about any topic, "
            "use the `search_everything` tool to query the web, gather key points from credible sources, "
            "and return a clear, concise answer in your own words. "
            "Always cite where you found the information."
        ),
        tools=[search_everything],
        handoff_description="→ Handing off to GoogleSearcher for detailed web research",
        model=model,
    )

    # Sub-agent for latest news and current events
    news_agent = Agent(
        name="NewsFetcher",
        instructions=(
            "You are NewsFetcher, an AI expert in current events. "
            "When a user requests the latest news, breaking updates, or recent developments, "
            "use the `fetch_latest_news` tool to retrieve top headlines from trustworthy outlets, "
            "then summarize the main points and include publication dates."
        ),
        tools=[fetch_latest_news],
        handoff_description="→ Handing off to NewsFetcher for up-to-date news",
        model=model,
    )

    # Top-level assistant that decides routing or answers directly
    assistant = Agent(
        name="Assistant",
        instructions=(
            
            "You are Assistant, a helpful general-purpose AI. For each user query:\n"
            "  • If they ask for factual information, definitions, or detailed explanations (e.g. “What is X?”, “Explain Y”)," \
            "If user asks for a definition, explanation, or factual information (e.g. “What is X?”, “Explain Y”), "
            "If user ask Create me a artical you can Create It self Dont hand off to GoogleSearcher\n"
            "use the GoogleSearcher handoff tool.\n"
            "  • If they ask for the latest news, headlines, or current events (e.g. “What’s happening now?”, “Latest on Z”), "
            "use the NewsFetcher handoff tool.\n"
            "  • Otherwise—such as creative requests, opinions, or conversational chat—answer directly yourself.\n"
            "Examples:\n"
            "  - “What’s the capital of France?” → GoogleSearcher\n"
            "  - “What are today’s top tech headlines?” → NewsFetcher\n"
            "  - “Tell me a joke.” → Assistant answers directly\n"
            "When you hand off, the system will print your handoff_description arrow."
        ),
        handoffs=[
            handoff(agent=google_agent),
            handoff(agent=news_agent),
        ],
        model=model,
    )

    return assistant
