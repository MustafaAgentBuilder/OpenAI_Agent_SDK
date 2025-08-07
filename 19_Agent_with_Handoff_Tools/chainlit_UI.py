import chainlit as cl
from agents import Runner
from chainlit.types import ThreadDict
from main import create_assistant_agent

@cl.on_chat_start
async def on_chat_start():
    # Initialize history as a list in user_session
    cl.user_session.set("history", [])
    await cl.Message(
        content="**Hello! I'm Mustafa Agent.** I remember our conversation history! How can I help? 😊",
        author="Assistant"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Safely get history from user_session (returns None if not exists)
    history = cl.user_session.get("history")
    with open("history.txt", "a") as file:
        file.write(f"User: {message.content}\n")
    
    # Ensure history is a list (in case it was None)
    if history is None:
        history = []
        cl.user_session.set("history", history)

    # Create assistant message
    Aimsg = cl.Message(content="", author="Assistant")
    await Aimsg.send()

    # Add user message to history
    user_message = {"role": "user", "content": message.content}
    history.append(user_message)

    try:
        agent = create_assistant_agent()
        # Pass the entire history to the agent instead of just the current message
        result = Runner.run_streamed(
            agent,
            input=history  # Changed from input=message.content to input=history
        )

        full_response = []
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                full_response.append(token)
                await Aimsg.stream_token(token)

        # Add assistant response to history
        assistant_response = ''.join(full_response)
        history.append({"role": "assistant", "content": assistant_response})
        
        # Update the history in user_session
        cl.user_session.set("history", history)
        await Aimsg.update()

    except Exception as e:
        await cl.Message(
            content=f"⚠️ Error: {str(e)}",
            author="System"
        ).send()
        raise

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    # Properly handle history restoration
    history = thread.get("history", [])
    cl.user_session.set("history", history)