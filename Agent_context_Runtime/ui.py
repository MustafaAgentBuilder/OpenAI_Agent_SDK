import chainlit as cl
from main import ai_agent, UserInfo
from agents import Runner

@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Hello! I'm your Assistant agent.").send()
    cl.user_session.set("chat_history", [])
    # Initialize user_info and store it in the session
    user_info = UserInfo(
        name="Unknown",
        age=0,
        location="Unknown",
        interests=[],
        preferences={}
    )
    cl.user_session.set("user_info", user_info)

@cl.on_message
async def main(message: cl.Message):
    # 1) Load and update history
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    # 2) Get a fresh agent and the shared context from the session
    agent, _ = await ai_agent()  # Ignore the default user_info from ai_agent
    user_info = cl.user_session.get("user_info")  # Use the persistent context

    # 3) Run the agent, passing in the mutable context
    response = Runner.run_streamed(
        starting_agent=agent,
        input=history,
        context=user_info
    )

    # 4) Create and send a placeholder message
    msg = cl.Message(content="")
    await msg.send()

    # 5) Stream each token into the chat message
    async for event in response.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, "delta"):
            await msg.stream_token(event.data.delta)

    # 6) Save assistant’s reply back to history
    history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("chat_history", history)
    # Ensure user_info is updated in the session
    cl.user_session.set("user_info", user_info)