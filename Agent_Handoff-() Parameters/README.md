# `handoff()` Parameters Reference

This document lists every parameter you can pass to the `handoff()` function in the OpenAI Agents SDK, with simple explanations and code examples. Use this in your GitHub docs so others can understand quickly.

**OpenAi Agent Sdk Docs** : https://openai.github.io/openai-agents-python/handoffs/

---

## 1. `agent`

* **What it is:** The **target** agent you want to delegate to.
* **Type:** `Agent`
* **Required:** Yes

```python
from agents import Agent, handoff

# Create the target agent
referral_agent = Agent(name="Referral Agent")

# Use it in a handoff
referral_handoff = handoff(
    agent=referral_agent
)
```

*The LLM will call this agent when it invokes your handoff tool.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## 2. `tool_name_override`

* **What it is:** Custom name for the internal tool that the LLM calls (defaults to `transfer_to_<agent_name>`).
* **Type:** `str`
* **Required:** No

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing Agent")

custom_tool_handoff = handoff(
    agent=billing_agent,
    tool_name_override="escalate_to_billing"
)
```

*The LLM sees a tool named ****`escalate_to_billing`**** instead of the default.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## 3. `tool_description_override`

* **What it is:** Custom description for how the handoff tool shows up in the LLM’s toolbox.
* **Type:** `str`
* **Required:** No

```python
from agents import Agent, handoff

support_agent = Agent(name="Support Agent")

fancy_handoff = handoff(
    agent=support_agent,
    tool_description_override="Send user to Level 2 Support"
)
```

*Helps the LLM understand what that tool does.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## 4. `on_handoff`

* **What it is:** A callback function that runs **before** the LLM switches to the target agent.
* **Type:** `Callable`
* **Required:** No

```python
from agents import Agent, handoff, RunContextWrapper

async def log_and_forward(ctx: RunContextWrapper[None]):
    # Your custom logic here
    print("Handoff happening! Context:", ctx)
    # Return the agent to handle the rest
    return Agent(name="Next Agent")

handoff_with_callback = handoff(
    agent=Agent(name="Next Agent"),
    on_handoff=log_and_forward
)
```

*Useful to log, fetch data, or modify context.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## 5. `input_type`

* **What it is:** A Pydantic model specifying structured data the LLM must supply when invoking the handoff tool.
* **Type:** `BaseModel` subclass
* **Required:** No

```python
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str

async def handle_escalation(ctx: RunContextWrapper[None], data: EscalationData):
    print("User escalated because:", data.reason)

escalation_handoff = handoff(
    agent=Agent(name="Escalation Agent"),
    on_handoff=handle_escalation,
    input_type=EscalationData
)
```

*LLM must supply JSON matching ****`EscalationData`****.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## 6. `input_filter`

* **What it is:** A function that receives the upcoming agent’s raw history and returns a modified version. Great for removing noise.
* **Type:** `Callable[[HandoffInputData], HandoffInputData]`
* **Required:** No

```python
from agents import Agent, handoff
from agents.extensions import handoff_filters

faq_agent = Agent(name="FAQ Agent")

filtered_handoff = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools
)
```

*Here, any previous “tool call” messages get stripped out before ****`FAQ Agent`**** sees them.* ([openai.github.io](https://openai.github.io/openai-agents-python/handoffs/))

---

## Putting It All Together

```python
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

# 1) Define your Pydantic model
class UserData(BaseModel):
    user_id: int
    issue: str

# 2) Callback logic
async def my_callback(ctx: RunContextWrapper[None], data: UserData):
    print(f"User {data.user_id} handed off for: {data.issue}")
    return Agent(name="Issue Resolver")

# 3) Build your handoff
full_handoff = handoff(
    agent=Agent(name="Issue Resolver"),
    tool_name_override="resolve_issue",
    tool_description_override="Resolve user-reported issue",
    on_handoff=my_callback,
    input_type=UserData,
    input_filter=handoff_filters.remove_all_tools,
)

# 4) Use recommended prompt if desired
resolver_agent = Agent(
    name="Resolver",
    instructions=prompt_with_handoff_instructions(
        "Handle the issue using the tool above, then summarize the resolution."
    ),
    handoffs=[full_handoff]
)
```

Now you have a complete, documented example showing every `handoff()` parameter in action. Copy this `.md` directly into your GitHub README or docs site!

### Including Handoff Info in Prompts

This technique helps the **current agent** understand **when** and **how** to hand off to another agent. It adds instructions in the prompt telling the LLM (Language Model) what types of user requests should be sent to other agents.

🔍 **Main Purpose:**
We use this to guide the LLM in choosing the correct handoff automatically, without hard-coding logic. It helps keep the conversation natural and context-aware.

🧠 **How It Works:**
You use helper functions like `prompt_with_handoff_instructions()` or a prompt prefix like `RECOMMENDED_PROMPT_PREFIX`, and combine them with instructions inside your agent.

✅ **Example:**

```python
from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

billing_agent = Agent(
    name="Billing Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
If the user asks about invoices or billing problems, use the handoff tool. Otherwise, help as normal."""
)
```

This tells the agent: “If you see a billing-related question, hand it off using the tool.”
