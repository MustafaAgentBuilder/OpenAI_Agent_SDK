from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()
# We can create a simple chatbot with the use of OpenRouter API.
# This chatbot will be able to send messages to a user and receive messages from the user.

#Reference: https://openrouter.ai/docs/quickstart

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

# Some other free models on 26th March:
# https://openrouter.ai/deepseek/deepseek-chat-v3-0324:free
# https://openrouter.ai/google/gemini-2.5-pro-exp-03-25:free

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
response = requests.post(
  url=f"{BASE_URL}/chat/completions",
  headers={
    "Authorization": f"Bearer {openrouter_api_key}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

print(response.json())



data = response.json()
data['choices'][0]['message']['content']