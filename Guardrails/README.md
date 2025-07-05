## OpenAI Agents SDK: Guardrails Deep Study

### Introduction

This README is a **complete breakdown** of the Guardrails feature in the OpenAI Agents SDK. It combines a high-level overview, detailed explanations, beginner-friendly code examples, and context for learners preparing for a quiz or project. Content is derived from the official docs:

* [Guardrails Documentation](https://openai.github.io/openai-agents-python/guardrails/)
* [Guardrails Reference](https://openai.github.io/openai-agents-python/ref/guardrail/)

---

## 🔍 1. What Are Guardrails?

* **Guardrails** are safety checks you plug into an agent’s run.
* They monitor either the **input** (what you send to the agent) or the **output** (what the agent returns).
* If a guardrail detects something undesirable (off-topic, toxic, invalid, etc.), it can **halt** the agent or raise an exception.

**Types of Guardrails**:

* **Input Guardrails**: Validate user inputs before the agent processes them.
* **Output Guardrails**: Validate the agent’s final output.

---

## ⚙️ 2. Two Main Flavors

| Type                | When It Runs        | What It Sees                | Returns                 |
| ------------------- | ------------------- | --------------------------- | ----------------------- |
| **InputGuardrail**  | *Before* agent work | Raw user messages or inputs | `InputGuardrailResult`  |
| **OutputGuardrail** | *After* agent work  | Agent-generated outputs     | `OutputGuardrailResult` |

---

## 🔄 3. Core Flow in `Runner.run()`

1. **Prepare Context**
   Wrap history and variables in a `RunContextWrapper`.

2. **Input Checks**
   For each registered `InputGuardrail`, call `.run(context, agent, input)`.

   * If any returns `tripwire_triggered=True`, an exception halts execution.

3. **Agent Executes**
   If inputs pass, the agent runs (picks tools or generates text).

4. **Output Checks**
   For each `OutputGuardrail`, call `.run(context, agent, agent_output)`.

   * A tripwire here also stops and raises an exception.

5. **Final Response**
   If no tripwires trigger, return the agent’s response to the user.

---

## 🔗 4. How Everything Connects

```
Runner.run()
 ├─► InputGuardrail.run()  (many)
 │     └─► InputGuardrailResult ➞ GuardrailFunctionOutput
 ├─► Agent.do_work() ➞ agent_output
 ├─► OutputGuardrail.run() (many)
 │     └─► OutputGuardrailResult ➞ GuardrailFunctionOutput
 └─► Return final output (unless tripwire)
```

* **Decorators** (`@input_guardrail`, `@output_guardrail`) convert functions into guardrail objects.
* **`GuardrailFunctionOutput`** encapsulates check details and stop/no-stop flag.

---

## 🛠 5. Beginner-Friendly Code Examples

### Example 1: Input Guardrail for Math Homework

```python
# Check if input is math homework and stop agent if so
from pydantic import BaseModel
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail, input_guardrail
import asyncio

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

@input_guardrail
async def math_homework_guardrail(ctx, agent, user_input):
    result = await Runner.run(
        Agent(name="Math Check", instructions="Detect math homework.", output_type=MathHomeworkOutput),
        user_input,
        context=ctx.context
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework
    )

main_agent = Agent(
    name="SupportAgent",
    instructions="Help except homework requests.",
    input_guardrails=[InputGuardrail(guardrail_function=math_homework_guardrail)]
)

async def main():
    try:
        print(await Runner.run(main_agent, "What is 2+2?"))
    except Exception as e:
        print(e)

asyncio.run(main())
```

### Example 2: Output Guardrail for Banned Words

```python
# Check agent output for banned words
from dataclasses import dataclass
from typing import Any, List

@dataclass
class GuardrailFunctionOutput:
    output_info: Any
    tripwire_triggered: bool

@dataclass
class OutputGuardrailResult:
    guardrail: Any
    agent_output: str
    agent: Any
    output: GuardrailFunctionOutput

class OutputGuardrail:
    def __init__(self, banned_words: List[str]):
        self.banned_words = banned_words

    async def run(self, ctx, agent, agent_output: str) -> OutputGuardrailResult:
        found = [w for w in self.banned_words if w in agent_output]
        output = GuardrailFunctionOutput(
            output_info={"found": found},
            tripwire_triggered=bool(found)
        )
        return OutputGuardrailResult(self, agent_output, agent, output)
```

---

## 📚 6. Technical Reference

* **`GuardrailFunctionOutput`**: Holds `output_info` and `tripwire_triggered` flag.
* **`InputGuardrailResult`** / **`OutputGuardrailResult`**: Wrap a guardrail run and its output.
* **`InputGuardrail`** / **`OutputGuardrail`**: Classes with `.run()` methods that call your functions.
* **Decorators**: `@input_guardrail`, `@output_guardrail` simplify creating guardrails.
* **Exceptions**: `InputGuardrailTripwireTriggered`, `OutputGuardrailTripwireTriggered` stop execution.

---

## 👣 Next Steps

1. **Deep Dive Classes**: Explore each class (`...FunctionOutput`, `...Guardrail`, etc.).
2. **Custom Guardrails**: Write your own checks using decorators.
3. **Quiz**: Test your knowledge with a series of MCQs on guardrail behavior.
4. **Project**: Integrate guardrails into your AI agent for safety and cost savings.

---

*By merging high‑level overview with detailed examples, this guide helps beginners and advanced learners alike to master Guardrails in the OpenAI Agents SDK.*
