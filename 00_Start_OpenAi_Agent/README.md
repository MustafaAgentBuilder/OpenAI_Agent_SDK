# AI Assistant SDK Example

This repository demonstrates how to build an AI assistant using an open-source SDK. The code shows how to set up the API provider, create a model, and run queries using both synchronous and asynchronous methods, including streaming responses.

## Overview

The code in this project helps you:
- Configure an API provider using environment variables.
- Set up a chat completion model.
- Create an AI assistant agent.
- Execute queries synchronously, asynchronously, and with streaming responses.

## Requirements

- **Python 3.7+**
- **Python dotenv:** Used to load environment variables from a `.env` file.
- **SDK Library:** Contains classes like `Agent`, `Runner`, `OpenAIChatCompletionsModel`, and `AsyncOpenAI`.
- **API Key:** You need an API key for the service, stored in a `.env` file as `GEMINI_API_KEY`.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the root directory with your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Code Explanation

### 1. Importing Modules and Setting Up the Environment
- **Modules Imported:**  
  The code imports necessary classes from the SDK, the dotenv package to load environment variables, and Python's built-in modules.
- **Environment Setup:**  
  It loads the environment variables from the `.env` file and disables extra tracing/logging to keep the output clean.

### 2. Configuring the API Provider and Model
- **API Provider:**  
  An instance of `AsyncOpenAI` is created using your API key and the base URL for the service.
- **Chat Completion Model:**  
  The `OpenAIChatCompletionsModel` is configured with the model "gemini-2.0-flash-exp" and the API provider.

### 3. Synchronous vs. Asynchronous Functions
- **Synchronous Functions:**  
  These run one after the other. Each function completes before the next one starts.  
  _Example:_ `make_coffee()` → `eat_breakfast()` → `drive_to_work()`
- **Asynchronous Functions:**  
  These functions can run concurrently using an event loop. They allow your program to perform other tasks while waiting for operations (like network calls) to complete.  
  _Example:_ Start laundry, then prepare dinner while laundry is running.

### 4. Runner Methods
- **`run_sync()`:**  
  A synchronous method to execute an agent and get the final output directly.
- **`run()`:**  
  An asynchronous method that must be called with `await` inside an async function.
- **`run_streamed()`:**  
  A streaming method that returns parts of the response as they are generated. This is useful when you want to see the response in real-time.

### 5. Code Examples
- **Synchronous Example (`run()` function):**
  - Creates an agent with instructions and uses `Runner.run_sync()` to process the query "Tell me about Pak Army."
  - Prints the final output.
- **Asynchronous Example (`new()` function):**
  - Creates an agent and uses `Runner.run()` with `await` to process the query "Tell me about yourself?"
  - Prints the final output.
- **Streaming Example (`stream_example()` function):**
  - Creates an agent and uses `Runner.run_streamed()` to process the query "Tell me a short story."
  - Prints parts of the story as they are received.

## How to Run

### Running the Asynchronous Example
To run the asynchronous example, simply execute your Python script:
```bash
python your_script_name.py
```
This will run the `new()` function and print the response from the assistant.

### Running the Streaming Example
If you want to see the streaming example in action, call the `stream_example()` function inside an async context similarly.

## Conclusion

This project gives you a clear starting point to work with an AI assistant SDK. It covers the basics of setting up an API provider, using asynchronous programming, and handling streaming responses. You can modify the code and experiment with it to learn more about asynchronous operations and API interactions in Python.

Happy coding! :)