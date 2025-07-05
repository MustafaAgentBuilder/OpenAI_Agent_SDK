# ChattyAgent with OpenAI Agents SDK

A simple Python-based AI assistant built using the OpenAI Agents SDK. Demonstrates dynamic prompts, lifecycle hooks, and custom model integration.

## 🚀 Features

- **Dynamic Instructions**  
  Build custom system prompts at runtime using user context (`RunContextWrapper`)

- **Context Mutation & Tools**  
  Store/update user data (user_id, user_name) across multiple agent runs

- **Lifecycle Hooks**  
  Intercept key events:
  - `on_agent_start`
  - `before_tool_calling`
  - `before_message_sending`
  - `on_agent_end`

- **Add logging to track the agent’s behavior.**
        
    Enable debugging to troubleshoot issues.
    
    `Inject custom behavior at key points, enhancing flexibility and control.`

- **For example,** 
    
    `in the code, MyDebugHooks prints a message when the agent starts, helping developers monitor its activity.`

- **Custom Model Support**  
  Example integration with Google's Gemini via `LitellmModel`

### Lifecycle Hooks Purpose
```python
class MyDebugHooks(AgentHooks[UserDynamic]):
    async def on_agent_start(self, context, **kwargs):
        print("Starting agent...", context.context.user_id)
```

* Add logging/debugging
* Inject custom behavior
* Monitor agent activity

## 📦 Installation
1. Clone repository:
```bash
git clone https://github.com/your-username/chatty-agent.git
cd chatty-agent
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## ⚙️ Usage

### 1. Define Context Model
```python
@dataclass
class UserDynamic:
    user_id: str
    user_name: str
```

### 2. Create Dynamic Prompts
```python
def dynamic_instructions(ctx, agent):
    fixed = "You are a knowledgeable Python tutor.\nAnswer step-by-step.\n"
    dynamic = f"User's name: {ctx.context.user_name}\n"
    return fixed + dynamic
```

### 3. Implement Hooks
```python
class MyDebugHooks(AgentHooks[UserDynamic]):
    async def on_agent_start(self, context, **kwargs):
        print(f"Agent started for {context.context.user_id}")
```

### 4. Run Agent
```python
agent = Agent[UserDynamic](
    name="ChattyAgent",
    model=LitellmModel(model="gemini-1.5-flash-latest"),
    instructions=dynamic_instructions,
    hooks=MyDebugHooks()
)

result = await Runner.run(
    starting_agent=agent,
    input="Fun fact about sloths?",
    context=user_ctx
)
```

## 🔍 Examples & Patterns
Explore official SDK examples:
* Basic: Dynamic prompts & streaming
* Tool Integration: Web search/file tools
* Multi-Agent Workflows: Agent coordination
* Voice Agents: TTS/STT integration

## 🤝 Contributing
1. Fork repo
2. Create feature branch:
```bash
git checkout -b feature/my-new-hook
```

3. Commit changes:
```bash
git commit -am 'Add awesome feature'
```

4. Push branch:
```bash
git push origin feature/my-new-hook
```

5. Open Pull Request - explain your changes!

## 📫 Contact
**Need Help?** Open an issue or reach out to mustafa786adeel@gmail.com