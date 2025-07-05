# OpenAI Agents SDK: Guardrails Deep Study

## Introduction
This README summarizes the educational content for the **"OpenAI SDK: Deep Study"** series, focusing on the **Guardrails** feature of the OpenAI Agents SDK. The series aims to help beginners understand Guardrails through clear explanations, beginner-friendly code examples, and a graduate-level quiz. The content is derived from the official documentation:
- [Guardrails Documentation](https://openai.github.io/openai-agents-python/guardrails/)
- [Guardrails Reference](https://openai.github.io/openai-agents-python/ref/guardrail/)

The goal is to prepare learners for a complex quiz . Below, we cover Guardrails' purpose, functionality, code examples, and a quiz to test understanding.

## What Are Guardrails?
Guardrails are a safety mechanism in the OpenAI Agents SDK to validate user inputs and agent outputs, ensuring AI applications are safe, relevant, and efficient. They run in parallel with agents, checking content and triggering a **tripwire** to halt execution if issues are detected. There are two types:
- **Input Guardrails**: Validate user input to prevent off-topic or malicious requests (e.g., math homework in a customer support app).
- **Output Guardrails**: Check the agent's final output to ensure it meets safety and validity standards.

### How Guardrails Work
1. **Input Guardrail**:
   - Checks user input before the agent processes it.
   - If invalid, triggers an `InputGuardrailTripwireTriggered` exception.
   - Only runs for the first agent in a workflow.
2. **Output Guardrail**:
   - Validates the agent's final output.
   - If invalid, triggers an `OutputGuardrailTripwireTriggered` exception.
   - Only runs for the last agent in a workflow.
3. **Configuration**: Guardrails are attached to specific agents, as different agents may require different validation rules.
4. **Parallel Execution**: Guardrails run alongside agents, reducing processing costs by stopping invalid requests early.

### Benefits
- **Cost Saving**: Prevents expensive model runs for invalid inputs/outputs.
- **Safety**: Filters inappropriate or malicious content.
- **Readability**: Integrates validation logic within agent code.
- **Flexibility**: Supports custom validation via Pydantic models and guardrail functions.

## Code Examples
Three beginner-friendly Python code examples demonstrate Guardrails in action. Each uses `asyncio`, Pydantic models, and the SDK's `Agent`, `Runner`, and guardrail decorators (`@input_guardrail`, `@output_guardrail`).

### Example 1: Input Guardrail for Math Homework
This example checks if user input is math homework-related, preventing misuse of a customer support agent.

**Code**: `input_guardrail_example.py`
```python
from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail, input_guardrail
import asyncio

# Pydantic model for guardrail output
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# Guardrail agent to check if input is math homework
guardrail_agent = Agent(
    name="Math Homework Check",
    instructions="Check if the user input is asking for math homework help.",
    output_type=MathHomeworkOutput
)

# Guardrail function
@input_guardrail
async def math_homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_math_homework
    )

# Main agent for handling user requests
main_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. Help users with their queries unless it's math homework.",
    input_guardrails=[InputGuardrail(guardrail_function=math_homework_guardrail)]
)

# Main function to run the agent
async def main():
    try:
        # Test with non-math input
        result = await Runner.run(main_agent, "How can I reset my password?")
        print("Result:", result.final_output)

        # Test with math homework input
        result = await Runner.run(main_agent, "Solve 2x + 3 = 7 for x.")
        print("Result:", result.final_output)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
```

**Output**:
```
Result: Here's how to reset your password: Go to the login page and click 'Forgot Password'.
Error: InputGuardrailTripwireTriggered: Guardrail math_homework_guardrail triggered
```

**Explanation**:
- A Pydantic model (`MathHomeworkOutput`) defines the guardrail output.
- A guardrail agent checks for math-related input.
- The main agent has an input guardrail that triggers an exception for math homework queries.

### Example 2: Output Guardrail for Math Content
This example ensures the agent's output does not contain math-related content.

**Code**: `output_guardrail_example.py`
```python
from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, OutputGuardrail, output_guardrail
import asyncio

# Pydantic model for guardrail output
class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

# Pydantic model for agent output
class MessageOutput(BaseModel):
    response: str

# Guardrail agent to check output
guardrail_agent = Agent(
    name="Math Output Check",
    instructions="Check if the output contains math-related content.",
    output_type=MathOutput
)

# Output guardrail function
@output_guardrail
async def math_output_guardrail(ctx, agent, output: MessageOutput):
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math
    )

# Main agent
main_agent = Agent(
    name="Response Agent",
    instructions="Respond to user queries.",
    output_type=MessageOutput,
    output_guardrails=[OutputGuardrail(guardrail_function=math_output_guardrail)]
)

# Main function
async def main():
    try:
        # Test with non-math output
        result = await Runner.run(main_agent, "Tell me about the weather.")
        print("Result:", result.final_output.response)

        # Test with math output
        result = await Runner.run(main_agent, "What is 2 + 2?")
        print("Result:", result.final_output.response)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
```

**Output**:
```
Result: The weather is sunny today!
Error: OutputGuardrailTripwireTriggered: Guardrail math_output_guardrail triggered
```

**Explanation**:
- Pydantic models (`MathOutput`, `MessageOutput`) structure guardrail and agent outputs.
- A guardrail agent validates the output for math content.
- The main agent triggers an exception if the output is math-related.

### Example 3: Input and Output Guardrails for Inappropriate Language
This example checks both user input and agent output for inappropriate language.

**Code**: `guardrails_example.py`
```python
from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail, OutputGuardrail, input_guardrail, output_guardrail
import asyncio

# Pydantic model for input guardrail output
class InappropriateInput(BaseModel):
    has_bad_language: bool
    reasoning: str

# Pydantic model for agent output
class ChatResponse(BaseModel):
    message: str

# Pydantic model for output guardrail
class InappropriateOutput(BaseModel):
    has_bad_language: bool
    reasoning: str

# Input guardrail agent to check for inappropriate language
input_guardrail_agent = Agent(
    name="Input Language Check",
    instructions="Check if the user input contains inappropriate or offensive language.",
    output_type=InappropriateInput
)

# Output guardrail agent to check agent output
output_guardrail_agent = Agent(
    name="Output Language Check",
    instructions="Check if the agent's output contains inappropriate or offensive language.",
    output_type=InappropriateOutput
)

# Input guardrail function
@input_guardrail
async def check_input_language(ctx, agent, input_data):
    result = await Runner.run(input_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.has_bad_language
    )

# Output guardrail function
@output_guardrail
async def check_output_language(ctx, agent, output: ChatResponse):
    result = await Runner.run(output_guardrail_agent, output.message, context=ctx.context)
    final_output = result.final_output
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.has_bad_language
    )

# Main agent for handling user queries
main_agent = Agent(
    name="Chat Agent",
    instructions="Respond to user queries politely and professionally. Avoid inappropriate language.",
    output_type=ChatResponse,
    input_guardrails=[InputGuardrail(guardrail_function=check_input_language)],
    output_guardrails=[OutputGuardrail(guardrail_function=check_output_language)]
)

# Main function to test the guardrails
async def main():
    try:
        # Test with clean input
        print("Testing clean input:")
        result = await Runner.run(main_agent, "How do I update my profile?")
        print("Response:", result.final_output.message)

        # Test with inappropriate input
        print("\nTesting inappropriate input:")
        result = await Runner.run(main_agent, "This app is stupid and terrible!")
        print("Response:", result.final_output.message)
    except Exception as e:
        print("Error:", str(e))

    try:
        # Test with clean output
        print("\nTesting clean output:")
        result = await Runner.run(main_agent, "What is the weather like?")
        print("Response:", result.final_output.message)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
```

**Output**:
```
Testing clean input:
Response: To update your profile, go to the settings page and click 'Edit Profile'.

Testing inappropriate input:
Error: InputGuardrailTripwireTriggered: Guardrail check_input_language triggered

Testing clean output:
Response: The weather is clear and sunny today!
```

**Explanation**:
- Pydantic models (`InappropriateInput`, `ChatResponse`, `InappropriateOutput`) define guardrail and agent outputs.
- Separate guardrail agents check input and output for inappropriate language.
- The main agent uses both input and output guardrails, triggering exceptions for invalid content.

## Quiz: Guardrails Knowledge Assessment
A 20-question multiple-choice quiz was created to test graduate-level understanding of Guardrails. Below is the quiz with answers.

**Quiz**: `guardrails_quiz.md`
```markdown
# OpenAI Agents SDK Guardrails Quiz

## Instructions
- This quiz contains 20 multiple-choice questions.
- Each question has four options, with only one correct answer.
- The quiz is designed for graduate-level understanding of the OpenAI Agents SDK Guardrails.

---

1. What is the primary purpose of guardrails in the OpenAI Agents SDK?
   - A) To enhance the agent's response speed
   - B) To validate and check user input or agent output
   - C) To manage agent handoffs
   - D) To generate structured data output

2. How many types of guardrails are supported by the OpenAI Agents SDK?
   - A) One
   - B) Two
   - C) Three
   - D) Four

3. When do input guardrails execute in a workflow?
   - A) Only when the agent is the last agent
   - B) Only when the agent is the first agent
   - C) For every agent in the workflow
   - D) After the agent produces its final output

4. What happens when a guardrail's tripwire is triggered?
   - A) The agent continues execution
   - B) An exception is raised, halting the agent's execution
   - C) The guardrail logs the issue and proceeds
   - D) The agent switches to a different model

5. Which exception is raised when an input guardrail's tripwire is triggered?
   - A) OutputGuardrailTripwireTriggered
   - B) InputGuardrailTripwireTriggered
   - C) GuardrailExecutionError
   - D) AgentHandoffError

6. What is the role of the `GuardrailFunctionOutput` class?
   - A) To define the agent's instructions
   - B) To store the result of a guardrail function
   - C) To manage handoffs between agents
   - D) To configure the agent's model settings

7. Why are guardrails configured on the agent itself?
   - A) To reduce the SDK's memory usage
   - B) Because different agents require different guardrails
   - C) To simplify the Runner class
   - D) To enable parallel execution of all agents

8. Which decorator is used to create an input guardrail function?
   - A) `@output_guardrail`
   - B) `@input_guardrail`
   - C) `@guardrail_function`
   - D) `@agent_guardrail`

9. What is the benefit of running guardrails in parallel to agents?
   - A) It increases the agent's response time
   - B) It reduces the cost of running expensive models
   - C) It simplifies the agent's instructions
   - D) It eliminates the need for handoffs

10. Which of the following is a valid use case for input guardrails?
    - A) Checking if the agent's output is math-related
    - B) Validating if the user input is off-topic
    - C) Ensuring the agent uses a specific tool
    - D) Modifying the agent's final output

11. What does the `tripwire_triggered` field in `GuardrailFunctionOutput` indicate?
    - A) Whether the guardrail function executed successfully
    - B) Whether the agent's output is structured
    - C) Whether the guardrail detected an issue
    - D) Whether the agent completed its task

12. In which scenario would an output guardrail NOT execute?
    - A) When the agent is the last agent in the workflow
    - B) When the agent is the first agent in the workflow
    - C) When the agent produces a final output
    - D) When the output is structured

13. What is the purpose of the `output_info` field in `GuardrailFunctionOutput`?
    - A) To store the agent's instructions
    - B) To provide optional information about the guardrail's checks
    - C) To define the agent's output type
    - D) To manage the agent's context

14. How can you disable tracing for a single guardrail run?
    - A) Set `OPENAI_AGENTS_DISABLE_TRACING=1`
    - B) Set `RunConfig.tracing_disabled=True`
    - C) Remove the guardrail from the agent
    - D) Use the `@no_tracing` decorator

15. Which Pydantic model is commonly used to define the structure of guardrail output?
    - A) AgentOutput
    - B) BaseModel
    - C) GuardrailModel
    - D) RunnerOutput

16. What is the default behavior when a guardrail function does not specify a name?
    - A) The SDK generates a random name
    - B) The function's name is used
    - C) The guardrail fails to execute
    - D) The agent's name is used

17. Which of the following is NOT a benefit of guardrails?
    - A) Cost saving by avoiding expensive model runs
    - B) Enhanced safety by filtering malicious content
    - C) Automatic generation of agent instructions
    - D) Improved code readability

18. How does the SDK handle guardrail functions that are asynchronous?
    - A) It converts them to synchronous functions
    - B) It supports them using `MaybeAwaitable`
    - C) It ignores them
    - D) It raises a syntax error

19. What is the role of the `RunContextWrapper` in a guardrail function?
    - A) To store the agent's output
    - B) To provide context and agent information
    - C) To define the guardrail's tripwire
    - D) To manage the agent's tools

20. Which component is responsible for running guardrails in the OpenAI Agents SDK?
    - A) Agent
    - B) Runner
    - C) Tool
    - D) Handoff

---

## Answers

1. B) To validate and check user input or agent output
2. B) Two
3. B) Only when the agent is the first agent
4. B) An exception is raised, halting the agent's execution
5. B) InputGuardrailTripwireTriggered
6. B) To store the result of a guardrail function
7. B) Because different agents require different guardrails
8. B) `@input_guardrail`
9. B) It reduces the cost of running expensive models
10. B) Validating if the user input is off-topic
11. C) Whether the guardrail detected an issue
12. B) When the agent is the first agent in the workflow
13. B) To provide optional information about the guardrail's checks
14. B) Set `RunConfig.tracing_disabled=True`
15. B) BaseModel
16. B) The function's name is used
17. C) Automatic generation of agent instructions
18. B) It supports them using `MaybeAwaitable`
19. B) To provide context and agent information
20. B) Runner
```

**Explanation**:
- The quiz tests technical knowledge, including guardrail execution, exceptions, decorators, and SDK components.
- Answers are provided for self-assessment, ensuring learners can verify their understanding.

## Technical Reference
The [Guardrails Reference](https://openai.github.io/openai-agents-python/ref/guardrail/) provides additional details:
- **GuardrailFunctionOutput**: A Pydantic model with `output_info` (optional) and `tripwire_triggered` (boolean).
- **InputGuardrail** and **OutputGuardrail**: Classes to wrap guardrail functions.
- **Decorators**: `@input_guardrail` and `@output_guardrail` convert functions into guardrails.
- **Exceptions**: Triggered when tripwires are activated, halting execution.

## Summary
This README consolidates all Guardrails-related content for the "OpenAI SDK: Deep Study" series:
- **Explanations**: Guardrails ensure safety and efficiency by validating inputs/outputs.
- **Code Examples**: Three examples demonstrate input/output guardrails for math homework and inappropriate language.
- **Quiz**: A 20-question MCQ challenges graduate-level learners.
- **Purpose**: Prepares beginners for a post-Eid quiz while providing practical, executable code.

Learners are encouraged to run the code examples and review the quiz to deepen their understanding. The series will continue after Eid with additional SDK features.