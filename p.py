from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()   # Load .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))   # <--- FIXED

models = client.models.list()

print("\n=== AVAILABLE GROQ MODELS ===")
for m in models.data:
    print(m.id)
