# OpenAI Agent with LiteLLM Integration

This project demonstrates how to integrate OpenAI's Agent SDK with LiteLLM to use different language models (like Gemini) with the OpenAI Agents framework.

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install openai-agents litellm python-dotenv
   ```

## Configuration

1. Create a `.env` file in the root directory with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MODEL=gemini-pro
   ```

## Common Issues and Solutions

### UnicodeDecodeError on Windows

When running with LiteLLM on Windows, you might encounter this error:

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81
```

This happens because Windows uses `cp1252` as the default encoding, but LiteLLM reads JSON files containing special characters without specifying the encoding.

#### Temporary Fix

Add this to the top of your `main.py`:

```python
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
```

Or set this environment variable before running your script:

```bash
set PYTHONIOENCODING=utf-8
python main.py
```

#### Permanent Fix (Recommended)

1. Navigate to the LiteLLM utils file in your virtual environment:
   ```
   venv\Lib\site-packages\litellm\utils.py
   ```

2. Find this line (around line 188):
   ```python
   json_data = json.load(f)
   ```

3. Change it to:
   ```python
   json_data = json.load(f, encoding='utf-8')
   ```

   Or alternatively:
   ```python
   with open(filename, encoding='utf-8') as f:
       json_data = json.load(f)
   ```

### Stay Updated

Make sure you're using the latest version of LiteLLM, which includes many bug fixes:

```bash
pip install --upgrade litellm
```

## Sample Code

```python
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
```