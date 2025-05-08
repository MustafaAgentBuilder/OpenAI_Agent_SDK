# OpenRouter Agent Framework

A simple way to use multiple AI models through OpenRouter's unified API.

## Overview

This package demonstrates how to use the `agents` framework with OpenRouter to access various AI models through a consistent interface. It provides a high-level abstraction that makes it easy to switch between models from different providers without changing your code structure.

## Features

- **Model Flexibility**: Switch between models from Google, Anthropic, OpenAI, and others with a simple string change
- **Async Support**: Built with async processing for better performance
- **Structured Interactions**: Define agent behaviors with clear instructions
- **Unified API**: No need to learn different APIs for each provider

## Installation

```bash
# Install the required packages
pip install agents openai python-dotenv
```

## Setup

1. Sign up for an [OpenRouter](https://openrouter.ai/) account
2. Get your API key from the OpenRouter dashboard
3. Create a `.env` file in your project root with:

```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage Example

```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Setup OpenRouter connection
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = "https://openrouter.ai/api/v1"
openrouter_model = "google/gemini-2.0-flash-lite-preview-02-05:free"

# Create provider client
provider = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url=openrouter_base_url,
)

async def main():
    # Create an agent
    agent = Agent(
        name="OpenRouter Assistant",
        instructions="You are a helpful AI assistant.",
        model=OpenAIChatCompletionsModel(
            model=openrouter_model,
            openai_client=provider
        )
    )
    
    # Run the agent with a question
    response = await Runner.run(
        starting_agent=agent,
        input="What are three interesting facts about space exploration?",
    )
    
    # Print the response
    print(response.final_output)

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
```

## Available Models

OpenRouter provides access to many models. Here are some free ones you can try:

- `google/gemini-2.0-flash-lite-preview-02-05:free`
- `anthropic/claude-3-haiku:free`
- `nvidia/llama-3.1-nemotron-nano-8b-v1:free`
- `mistralai/mistral-7b-instruct:free`

For a complete list, check the [OpenRouter models page](https://openrouter.ai/models).

## Comparison with Direct API Approaches

### OpenRouter vs Direct API Connection

Using OpenRouter with the agent framework offers several advantages over connecting directly to provider APIs:

#### Model Switching

**With OpenRouter:**
```python
# Switch models with a single line change
model = OpenAIChatCompletionsModel(
    model="google/gemini-2.0-flash-lite-preview-02-05:free",  # Google model
    openai_client=provider
)

# Later, switch to Claude
model = OpenAIChatCompletionsModel(
    model="anthropic/claude-3-haiku:free",  # Anthropic model
    openai_client=provider
)
```

**With Direct API:**
Need different code structures, libraries, and authentication methods for each provider.

#### Simplified Interface

OpenRouter provides a consistent interface across all models, so your code remains the same regardless of which model you're using.

## Best Practices

1. **Error Handling**: Always check if your API key is set before making requests
2. **Model Selection**: Choose the appropriate model for your task - some are better at coding, others at creative tasks
3. **Async Usage**: Leverage async capabilities for parallel requests when needed

## Troubleshooting

- **Authentication Error**: Make sure your OpenRouter API key is correct and properly set in the .env file
- **Model Not Found**: Check that the model name is correct and available on OpenRouter
- **Rate Limiting**: Free tier models have request limits - consider upgrading for production use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

