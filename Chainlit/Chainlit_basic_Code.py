from agents import Runner
from main import orcerstration_agent as agent
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl


@cl.on_chat_start
async def start():
    cl.user_session.set('history',[])

@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(
        content ="",
    )
    await msg.send()
    f = open("history.txt", "a")
    f.write("User: " + message.content + "\n")
    history = cl.user_session.get("history")
    history.append({'role': 'user', 'content': message.content})
    
    ai_reponse =  Runner.run_streamed(agent, history)
    async for event in ai_reponse.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            raw_txt = event.data.delta
            await msg.stream_token(raw_txt)


    msg.content=ai_reponse.final_output
    await msg.update()
    history.append({'role': 'assistant', 'content': ai_reponse.final_output})
    cl.user_session.set("history", history)
    print("--------------------------------------")