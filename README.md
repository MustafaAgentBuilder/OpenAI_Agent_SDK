# OpenAI Agents SDK

## Overview

The OpenAI Agents SDK is a Python-based toolkit designed to simplify the creation and management of AI agents. These agents are powered by OpenAI's language models and can perform a variety of tasks, such as searching the web, processing documents, and operating computers on behalf of users. The SDK provides a structured framework that allows developers to build complex, multi-agent workflows efficiently.

## Key Features

### Agent Loop
The SDK includes a built-in agent loop that manages the process of calling tools, sending results to the language model, and repeating these steps until the task is complete. This feature automates much of the workflow, reducing the need for manual intervention.

### Python-First Approach
Designed with Python developers in mind, the SDK leverages Python's native features for orchestrating and chaining agents. This means you don't have to learn new abstractions, making it more intuitive and easier to integrate into existing Python projects.

### Handoffs
This feature enables seamless coordination and delegation between multiple agents. Agents can pass control to one another dynamically, facilitating complex workflows where different agents handle specific tasks.

### Guardrails
The SDK allows for input validations and checks to run in parallel with your agents. If any of these checks fail, the process can break early, ensuring that only valid data is processed and enhancing the safety and reliability of your AI agents.

### Tracing
Automatic tracing capabilities make it easy to track and debug the behavior of your agents. The SDK supports integration with various external tracing tools, providing flexibility in monitoring and logging.

## Components of the SDK

### Agents
At the core of the SDK are agents, which are large language models configured with specific instructions and tools to perform designated tasks. You can define the behavior of an agent by setting properties such as instructions (system prompts), the model to use, and the tools it can access.

### Runner
The Runner class is responsible for executing agents. It offers multiple methods to run agents:

- **run()**: An asynchronous method that returns a RunResult
- **run_sync()**: A synchronous method that wraps around the run() method, suitable for environments without an existing event loop
- **run_streamed()**: An asynchronous method that returns a RunResultStreaming, allowing for streaming responses as they are received

### Tools
Agents can be equipped with various tools to extend their capabilities. These tools can include web search functionalities, document retrieval systems, or custom functions that you define. Integrating tools enables agents to interact with external systems and perform a broader range of tasks.

### Function Tools
The SDK allows you to convert Python functions into tools that agents can use. By extracting metadata from function docstrings, the SDK can generate schemas that describe the function's name, description, and parameters, facilitating seamless integration with the agent's capabilities.

## Getting Started

To begin using the SDK, follow these steps:

### Installation
Install the SDK using pip:

### This version is the only one supported for my agent to run.
```bash
pip install openai-agents==0.0.7
```

### Setting Up an Agent
Define an agent by specifying its instructions, model, and tools:

```python
from agents import Agent, ModelSettings, function_tool

# Define a simple tool
@function_tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

# Configure the agent
agent = Agent(
    instructions="You are a friendly assistant.",
    model=ModelSettings(model="gpt-4"),
    tools=[greet]
)
```

### Running the Agent
Use the Runner class to execute the agent:

```python
from agents import Runner

# Run the agent synchronously
result = Runner.run_sync(starting_agent=agent, input="Greet John")
print(result)
```

## Conclusion

The OpenAI Agents SDK offers a robust framework for developing AI agents capable of performing a wide range of tasks. Its Python-first design, combined with features like agent loops, handoffs, guardrails, and tracing, makes it accessible and efficient for developers. Whether you're building simple assistants or complex multi-agent systems, the SDK provides the tools and structure needed to bring your AI projects to life.
