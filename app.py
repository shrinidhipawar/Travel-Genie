# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()

PERSIST_DIR = "chroma_db"
DEFAULT_MODEL = "llama-3.1-8b-instant"
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("Missing GROQ_API_KEY in .env")
    st.stop()

client = Groq(api_key=GROQ_KEY)

st.set_page_config(page_title="TravelGenie", layout="wide")
st.title("TravelGenie ✈️ — RAG Itinerary Planner")

# Sidebar
with st.sidebar:
    st.markdown("### Settings")
    model = st.text_input("Groq model", value=DEFAULT_MODEL)
    top_k = st.slider("Retriever top-k", 1, 10, 4)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.35)

st.markdown("Enter something like: `Paris, Rome / 5 days / food, museums`")

query = st.text_input("Ask something:")
run = st.button("Generate Itinerary")


# ------------------------------
# Parse Multi-City Query
# ------------------------------
def parse_query(q):
    parts = [p.strip() for p in q.split("/")]
    cities = parts[0].split(",")
    days = parts[1].strip() if len(parts) > 1 else "2 days"
    interests = parts[2].strip() if len(parts) > 2 else "general"
    return cities, days, interests


# ------------------------------
# MAIN LOGIC
# ------------------------------
if run:
    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    # Parse query
    cities, days, interests = parse_query(query)

    # Load DB
    try:
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        db = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings,
        )
    except Exception as e:
        st.error(f"Vector DB load error: {e}")
        st.stop()

    # Retrieve
    try:
        docs = db.similarity_search(query, k=top_k)
    except Exception as e:
        st.error(f"Retrieval error: {e}")
        st.stop()

    # Build context
    if docs:
        ctx_parts = []
        for i, d in enumerate(docs):
            src = d.metadata.get("source", f"chunk_{i}")
            excerpt = d.page_content.strip()
            if len(excerpt) > 600:
                excerpt = excerpt[:600] + "..."
            ctx_parts.append(f"Source ({src}):\n{excerpt}\n")

        context_text = "\n\n".join(ctx_parts)
    else:
        context_text = ""
        st.info("No RAG data found. Model may answer from general knowledge.")

    # Prompt
    prompt = f"""
You are TravelGenie, an expert RAG-based travel itinerary planner.

MULTI-CITY TRIP REQUEST:
Cities: {cities}
Trip Length: {days}
Interests: {interests}

CONTEXT (use ONLY this information):
{context_text}

RULES:
- If context lacks enough data, say so.
- Otherwise generate a structured, day-by-day itinerary.
- Each day must include Morning / Afternoon / Evening.
- Keep travel times realistic.
- Add suggested nearby food spots *only if mentioned in context*.

Now produce the itinerary.
"""

    # Groq call
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=float(temperature),
        )
        answer = response.choices[0].message.content  # FIXED: correct Groq accessor
    except Exception as e:
        st.error(f"Groq API error: {e}")
        st.stop()

    # Show result
    st.subheader("Generated Itinerary")
    st.markdown(answer)

    # Show retrieved context
    if docs:
        st.markdown("---")
        st.subheader("Retrieved Evidence")
        for i, d in enumerate(docs):
            st.markdown(f"**Source:** {d.metadata.get('source', f'chunk_{i}')}**")
            st.write(d.page_content)
