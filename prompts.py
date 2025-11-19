# prompts.py
from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate

ITINERARY_PROMPT = PromptTemplate(
    input_variables=["days", "preferences", "retrieved_snippets"],
    template=(
        "You are an expert travel planner. Using the information below (which contains local "
        "attractions, restaurants, and travel tips), build a realistic {days}-day itinerary "
        "for a traveler who likes: {preferences}.\n\n"
        "Guiding rules:\n"
        "- For each day produce Morning / Afternoon / Evening blocks.\n"
        "- For each block include: activity name, short description (1 sentence), estimated time, and suggested nearby food option.\n"
        "- Keep walking/transport times reasonable (no more than 30–45 mins between main stops per block).\n"
        "- Cite the source filename in parentheses if relevant.\n\n"
        "Here are context snippets:\n{retrieved_snippets}\n\n"
        "Now generate the itinerary."
    )
)
