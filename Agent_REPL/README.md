Great! You're working with an **OpenAI Agents SDK** example using **async**, `Agent`, `Runner`, and a custom tool. I’ll explain your code step-by-step **like documentation**, so you understand **what each part does** — great for learning and reuse.

---

## 📘 Full Documentation (for your code)

---

### ✅ 1. Imports

```python
import asyncio
from agents import Agent, Runner, function_tool
from agents.types import ChatMessage
```

* `asyncio`: Used to run asynchronous code (`async def`, `await`, etc.)
* `Agent`: Creates a smart assistant powered by OpenAI models.
* `Runner`: Executes the agent with input/output handling.
* `function_tool`: Converts a Python function into a tool the agent can use.
* `ChatMessage`: Represents a message from the user or assistant.

---

### ✅ 2. Define a Tool

```python
@function_tool
def get_greeting(name: str) -> str:
    """Returns a personalized greeting."""
    return f"Hello, {name}! How can I assist you today?"
```

* This is a **Python function** that becomes a **tool** the agent can use.
* `@function_tool` tells the agent: **“This is a callable tool.”**
* The docstring (`"""Returns..."""`) becomes the **tool description** the agent sees.

---

### ✅ 3. Create an Agent

```python
agent = Agent(
    name="Greeter",
    instructions="You are a friendly assistant. Use the get_greeting tool when appropriate.",
    tools=[get_greeting],
    model="gpt-4o"
)
```

* `name`: Internal name of the agent.
* `instructions`: Like a "prompt" — tells the agent how to behave.
* `tools`: A list of functions the agent can use (`get_greeting` in this case).
* `model`: The LLM model you want to use (`gpt-4o` in this example).

---

### ✅ 4. Async Interactive Loop

```python
async def interactive_loop() -> None:
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = await Runner.run(
            agent=agent,
            messages=[ChatMessage(content=user_input, role="user")],
            stream=False
        )
        print(f"Assistant: {result.final_output}")
```

This is a loop that:

* Waits for **user input** in the terminal.
* Sends the input to the **agent** using `Runner.run()`.
* The `ChatMessage` is used to wrap your input as a "user message".
* The `agent` may respond using the **tool** if it thinks it’s needed.
* `stream=False`: means the whole response is returned at once (not streamed token by token).

---

### ✅ 5. Main Async Entry Point

```python
async def main() -> None:
    await interactive_loop()

if __name__ == "__main__":
    asyncio.run(main())
```

* This is the **entry point** of your program.
* `asyncio.run(main())` starts the event loop and runs the whole thing asynchronously.

---

## ✅ What This Code Does

It runs a **terminal-based chat** with an **AI agent** that:

* Uses OpenAI’s `gpt-4o`
* Can call your Python function (`get_greeting`) as a **tool**
* Asks for user input in a loop until you type `"exit"`

---

## 🧠 Output Example

```bash
You: hi
Assistant: Hello! How can I assist you today?

You: my name is Mustafa
Assistant: Hello, Mustafa! How can I assist you today?

You: exit
```

If the LLM understands that "Mustafa" is your name, it might call the `get_greeting()` tool.

---

## 🔗 Related Concepts You Used

| Concept          | Your Code Example              | Explanation                                    |
| ---------------- | ------------------------------ | ---------------------------------------------- |
| `async`          | `async def interactive_loop()` | Non-blocking, allows you to await LLM response |
| `await`          | `await Runner.run(...)`        | Waits for the agent to respond                 |
| `@function_tool` | On `get_greeting`              | Makes the function available to the agent      |
| `Agent`          | `agent = Agent(...)`           | Defines the assistant's behavior and tools     |
| `Runner.run()`   | `await Runner.run(...)`        | Executes the agent and gets the response       |
| `ChatMessage`    | Wraps the user input           | Makes input compatible with the agent          |

---

## 📚 Want Official Docs?

Here’s where you can check **official documentation**:

* [🔗 OpenAI Agents SDK GitHub](https://github.com/openai/openagents)
* [🔗 Function calling with OpenAI tools](https://platform.openai.com/docs/guides/function-calling)
* [🔗 Asyncio in Python](https://docs.python.org/3/library/asyncio.html)

---

Let me know if you'd like to:

* Add **more tools** to your agent?
* Turn this into a **GUI app**?
* Log chats to a **file or database**?
* Stream responses like real-time typing?

I can help with any of these!
