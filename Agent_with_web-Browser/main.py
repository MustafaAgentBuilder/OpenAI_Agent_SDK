
# import asyncio
# import os

# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import SecretStr

# from browser_use import Agent, BrowserConfig
# from browser_use.browser.browser import Browser
# from browser_use.browser.context import BrowserContextConfig

# load_dotenv()
# api_key = os.getenv('GEMINI_API_KEY')
# if not api_key:
# 	raise ValueError('GEMINI_API_KEY is not set')

# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

# browser = Browser(
#     config=BrowserConfig(
#         new_context_config=BrowserContextConfig()  # Remove viewport_expansion here
#     )
#  )




# async def run_search():
# 	agent = Agent(
# 		task='search for the latest news about the ai',
# 		llm=llm,
# 		max_actions_per_step=4,
# 		browser=browser,
# 	)

# 	await agent.run(max_steps=25)


# if __name__ == '__main__':
# 	asyncio.run(run_search())

import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# Assuming these are the correct imports based on your usage
from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

# Using a generally available and capable model
# gemini-2.0-flash-exp might be internal/experimental
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=SecretStr(api_key))

# --- FIX: Initialize BrowserContextConfig without the unexpected argument ---
# The 'viewport_expansion' parameter caused the TypeError.
# If you specifically need viewport settings, consult the browser_use
# documentation for the correct parameter names for your installed version.
# Common options might involve a 'viewport' dictionary, e.g., viewport={'width': 1920, 'height': 1080}
context_config = BrowserContextConfig(
    # viewport_expansion=0, # <--- REMOVED THIS LINE
    # You can add other *valid* BrowserContextConfig parameters here if needed
)

browser = Browser(
    config=BrowserConfig(
        new_context_config=context_config # Pass the correctly configured context object
    )
)
# --- END FIX ---

async def run_search():
    agent = Agent(
        task='Open Moviebox.com and search Fast and furious 5', # Corrected typo 'the ai' -> 'ai'
        llm=llm,
        max_actions_per_step=4,
        browser=browser,
    )
    try:
        await agent.run(max_steps=25)
    finally:
        # Ensure the browser is closed gracefully, which might help
        # mitigate the "Event loop is closed" error, although it's
        # often a library-level cleanup timing issue.
        await browser.close()


if __name__ == '__main__':
    # Standard way to run the main async function
    try:
        asyncio.run(run_search())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    # The RuntimeError: Event loop is closed usually happens *after*
    # asyncio.run() completes and during Python's final cleanup.
    # It's often related to how libraries manage subprocesses (like the browser)
    # and doesn't typically require a fix in *your* main script code,
    # unless it causes functional problems or resource leaks.