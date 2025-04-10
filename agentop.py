import google.generativeai as genai
import agentops
from agentops import Client
from agentops.sdk.decorators import operation, agent
import os

# === API Keys (hardcoded) ===
GEMINI_API_KEY = ""
AGENTOPS_API_KEY = ""

# === Configure APIs ===
genai.configure(api_key=GEMINI_API_KEY)
agentops.init(api_key=AGENTOPS_API_KEY)

# === Confirm AgentOps is initialized ===
print("Client initialized?", Client().initialized)
print("Client config API key:", Client().config.api_key)

# === Define a simple Gemini-connected Agent ===
@agent
class MyAgent:
    @operation
    def run(self, message: str) -> str:
        response = model.generate_content(message)
        return response.text

# === Create the Gemini model ===
model = genai.GenerativeModel("gemini-1.5-flash")

# === Start AgentOps Session ===
session = agentops.start_session()
try:
    print("\n🔹 Synchronous generation:")
    response = model.generate_content("What are the three laws of robotics?")
    print(response.text)

    print("\n🔹 Streaming generation:")
    stream_response = model.generate_content(
        "Explain the concept of machine learning in simple terms.",
        stream=True,
    )
    for chunk in stream_response:
        print(chunk.text, end="")
    print()  # For newline after stream

    print("\n🔹 Another generation:")
    response = model.generate_content("What is the difference between supervised and unsupervised learning?")
    print(response.text)

    print("\n🔹 Running Agent operation:")
    agent = MyAgent()
    result = agent.run("Summarize the importance of neural networks.")
    print("Agent Result:", result)

    agentops.end_session(session=session)  # Close session properly

except Exception as e:
    print("❌ Error occurred:", e)
    agentops.end_session(session=session, status="error")
    raise
