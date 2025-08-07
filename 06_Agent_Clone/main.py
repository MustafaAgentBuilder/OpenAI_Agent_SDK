# agents_clone_example.py

from openai import AssistantAgent

# Step 1: Create the main base agent
main_agent = AssistantAgent(
    name="BaseAgent",
    instructions="Reply in a helpful and friendly way.",
    model="gpt-4",
    temperature=0.7,
    profile_picture_url="https://example.com/base.png"
)

# Step 2: Clone agents with different personalities
pirate_agent = main_agent.clone(
    name="PirateAgent",
    instructions="Talk like a pirate. Use words like 'Arrr!' and sailor slang.",
    profile_picture_url="https://example.com/pirate.png"
)

robot_agent = main_agent.clone(
    name="RobotAgent",
    instructions="Talk like a robot. Be logical and emotionless.",
    profile_picture_url="https://example.com/robot.png"
)

teacher_agent = main_agent.clone(
    name="TeacherAgent",
    instructions="Talk like a school teacher. Be kind and clear in explanations.",
    profile_picture_url="https://example.com/teacher.png"
)

# Step 3: Ask each agent the same question
question = "What is Python used for?"

# Step 4: Let each agent answer
base_reply = main_agent.run(question)
pirate_reply = pirate_agent.run(question)
robot_reply = robot_agent.run(question)
teacher_reply = teacher_agent.run(question)

# Step 5: Print the answers
print("🔵 Base Agent says:\n", base_reply)
print("\n🏴‍☠️ Pirate Agent says:\n", pirate_reply)
print("\n🤖 Robot Agent says:\n", robot_reply)
print("\n👩‍🏫 Teacher Agent says:\n", teacher_reply)
