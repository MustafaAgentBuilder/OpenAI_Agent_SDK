# These are agent are run in OpenAi Agent SDK version ==0.0.7
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, set_default_openai_client, set_default_openai_api

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please check your .env file.")

try:
    custom_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    set_tracing_disabled(True)
    set_default_openai_client(custom_client)
    # This is The replacement of OpenAiChatcompletion
    set_default_openai_api("chat_completions")

    teacher = Agent(
        name="Teacher",
        instructions="You are a teacher. Answer questions asked by the student.",
        model="thudm/glm-4-32b:free",  # Prefix removed
    )
    
    student = Agent(
        name="Student",
        instructions="You are a student. Ask the teacher a question.",
        model="shisa-ai/shisa-v2-llama3.3-70b:free",
    )

    async def main():
        try:
            print("Running teacher agent...")
            teacher_response = await Runner.run(teacher, input="Tell me about Pakistan?")
            print("Teacher says:", teacher_response.final_output)
            
            print("Running student agent...")
            student_response = await Runner.run(student, input="Pakistan is a beautiful country?")
            print("Student says:", student_response.final_output)
        except Exception as e:
            print(f"Error during agent execution: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(main())
    
except Exception as e:
    print(f"Error initializing OpenRouter client: {e}")
    import traceback
    traceback.print_exc()