# ui.py

import chainlit as cl
from main import ai_agent
from agents import Runner

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! I'm your Assistant agent.").send()
    cl.user_session.set("chat_history", [])

@cl.on_message
async def main(message: cl.Message):
    # 1) load history and append user
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    # 2) get your agent and its context
    agent, user_info = await ai_agent()

    # 3) call the agent, passing in context
    response = Runner.run_streamed(
        starting_agent=agent,
        input=history,
        context=user_info
    )

    # 4) prepare a new chat message and send it
    msg = cl.Message(content="")
    await msg.send()

    # 5) stream each token into that message
    async for event in response.stream_events():
        if event.type == "raw_response_event" and hasattr(event.data, "delta"):
            await msg.stream_token(event.data.delta)

    # 6) save assistant reply back to history
    history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("chat_history", history)
