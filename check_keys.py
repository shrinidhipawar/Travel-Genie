from dotenv import load_dotenv
import os

load_dotenv()

groq = os.getenv("GROQ_API_KEY")
geo = os.getenv("GEOAPIFY_API_KEY")

print(f"GROQ_API_KEY found: {bool(groq)}")
if groq:
    print(f"GROQ key starts with: {groq[:4]}...")

print(f"GEOAPIFY_API_KEY found: {bool(geo)}")
if geo:
    print(f"Geoapify key starts with: {geo[:4]}...")
