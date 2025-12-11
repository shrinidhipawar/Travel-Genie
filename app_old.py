import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import requests

load_dotenv()

# --- Configuration ---
PERSIST_DIR = "chroma_db"      # matches your ingest.py
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_KEY = os.getenv("GROQ_API_KEY")
OPENTRIPMAP_KEY = os.getenv("OPENTRIPMAP_KEY")
# Known city names based on your data files; used to avoid cross-city mixing
CITY_NAMES = ["hyderabad", "paris", "rome", "london", "bangalore", "mumbai", "delhi", "goa", "jaipur", "kolkata"]

if not GROQ_KEY:
    st.error("GROQ_API_KEY not found in .env!")
    st.stop()
if not OPENTRIPMAP_KEY:
    st.error("OPENTRIPMAP_KEY not found in .env!")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# --- Page Configuration ---
st.set_page_config(
    page_title="TravelGenie",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for beautiful styling ---
st.markdown("""
<style>
    /* Main background and font */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #FFE66D;
        --dark-bg: #1a1a1a;
        --light-bg: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3em;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .main-header p {
        font-size: 1.1em;
        margin: 10px 0 0 0;
        opacity: 0.95;
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }
    
    .search-container h2 {
        color: #FF6B6B;
        font-size: 1.5em;
        margin-bottom: 20px;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px 15px !important;
        font-size: 1em !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4ECDC4 !important;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 30px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Itinerary card */
    .itinerary-container {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    
    .itinerary-container h2 {
        color: #FF6B6B;
        border-bottom: 3px solid #4ECDC4;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    
    .day-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f4f8 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #4ECDC4;
    }
    
    .day-section h3 {
        color: #FF6B6B;
        margin-top: 0;
    }
    
    /* Evidence section */
    .evidence-box {
        background: #f0f7ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4ECDC4;
    }
    
    .evidence-box strong {
        color: #FF6B6B;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        color: #FF6B6B;
        font-size: 1.2em;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #4ECDC4;
    }
    
    /* Info message */
    .stInfo {
        background-color: #e8f4f8 !important;
        border-left: 4px solid #4ECDC4 !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #e8f5e9 !important;
        border-left: 4px solid #4CAF50 !important;
    }
    
    /* City grid */
    .city-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 10px;
        margin: 15px 0;
    }
    
    .city-badge {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A5A0 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        text-align: center;
        font-size: 0.9em;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .city-badge:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Main Header ---
st.markdown("""
<div class="main-header">
    <h1>🌍 TravelGenie</h1>
    <p>Your AI-Powered Travel Planning Assistant</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Model**")
        model = st.text_input("", value=DEFAULT_GROQ_MODEL, key="model_input")
    
    with col2:
        st.markdown("**Temperature**")
        temp = st.slider("", 0.0, 1.0, 0.35, key="temp_slider")
    
    st.markdown("---")
    st.markdown("**Retriever**")
    top_k = st.slider("Top Results (k)", 1, 8, 4, key="topk_slider")
    
    st.markdown("---")
    st.markdown("**Available Cities**")
    st.markdown(f"""
    <div class="city-grid">
        {''.join([f'<div class="city-badge">{city.capitalize()}</div>' for city in CITY_NAMES])}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 **Tip:** Enter query as: `City / Days / Preferences`\n\nExample: `Paris / 3 days / museums, food`")

# --- Main Search Section ---
st.markdown("""
<div class="search-container">
    <h2>🔍 Plan Your Journey</h2>
</div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "Enter your travel query:",
        placeholder="e.g., Bangalore / 3 days / tech hub, food, gardens",
        label_visibility="collapsed"
    )

with col2:
    run_btn = st.button("🚀 Generate", use_container_width=True)


# --- API Helper Function ---
def fetch_from_opentripmap(city: str, limit: int = 10) -> str:
    """Fetch top places in a city using OpenTripMap API."""
    try:
        geo_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENTRIPMAP_KEY}"
        geo_r = requests.get(geo_url).json()
        lat, lon = geo_r["lat"], geo_r["lon"]

        radius_url = (
            f"https://api.opentripmap.com/0.1/en/places/radius"
            f"?apikey={OPENTRIPMAP_KEY}&radius=10000&lon={lon}&lat={lat}&limit={limit}"
        )
        places_r = requests.get(radius_url).json()
        places = []
        for p in places_r.get("features", []):
            name = p["properties"].get("name")
            kind = p["properties"].get("kinds")
            if name:
                places.append(f"{name} ({kind})")
        return "\n".join(places) if places else "No notable places found."
    except Exception as e:
        return f"Error fetching data from API: {e}"


# --- Main ---
if run_btn:
    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    query_lower = query.lower()
    # Try to detect city from known names inside the query; fall back to first token
    city = next((c for c in CITY_NAMES if c in query_lower), None)
    if not city:
        city = query.split("/")[0].split(",")[0].split("for")[0].strip().lower()

    # --- Load Chroma DB ---
    try:
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    except Exception as e:
        st.error(f"Error loading vector DB: {e}")
        st.stop()

    # --- Retrieve relevant chunks ---
    # Use similarity_search_with_score to get distance scores
    # Lower score = better match (for Euclidean/Cosine distance in Chroma default)
    results = db.similarity_search_with_score(query, k=top_k)

    # Filter by threshold AND city matching to avoid wrong city data
    RELEVANCE_THRESHOLD = 0.6  # Strict threshold
    
    valid_docs = []
    for doc, score in results:
        source = doc.metadata.get('source', '').lower()
        content = doc.page_content.lower()
        # Accept if score is good AND source/content match the detected city
        if score < RELEVANCE_THRESHOLD and (not city or city in source or city in content):
            valid_docs.append((doc, score))

    if valid_docs:
        # --- LOCAL RAG FOUND ---
        context_text = "\n\n".join(
            [f"Source ({d.metadata.get('source', 'chunk')}): {d.page_content}" for d, s in valid_docs]
        )
        mode = "LOCAL VECTOR DB"
        docs = [d for d, s in valid_docs] # Keep for display
    else:
        # --- FALLBACK TO API ---
        fallback_city = city if city else query
        st.info(f"No relevant local data found for {fallback_city}. Fetching live info from OpenTripMap API...")
        context_text = fetch_from_opentripmap(fallback_city)
        mode = "LIVE API"
        docs = []

    # --- Build prompt for Groq ---
    prompt = f"""
You are TravelGenie — a travel planner.

MODE USED: {mode}

CONTEXT:
{context_text}

USER REQUEST:
{query}

OUTPUT FORMAT:
- Short headline
- Day-by-day itinerary (Morning / Afternoon / Evening)
- Include one-sentence description for each item
- Suggest nearby places to eat if available
- Keep travel times reasonable
"""

    # --- Call Groq ---
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are TravelGenie, an expert travel planner."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=float(temp),
        )
        answer = response.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API error: {e}")
        st.stop()

    # --- Display Results ---
    st.markdown("")
    
    # Display mode indicator
    if mode == "LOCAL VECTOR DB":
        st.success(f"✅ **Using Local Knowledge Base** • {len(docs)} sources found")
    else:
        st.warning(f"🌐 **Using Live Data** • OpenTripMap API")
    
    st.markdown("""
    <div class="itinerary-container">
    """, unsafe_allow_html=True)
    
    st.markdown(f"## ✈️ Your Personalized Itinerary", unsafe_allow_html=True)
    st.markdown(answer)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show retrieved evidence
    if docs:
        st.markdown("---")
        with st.expander("📚 View Source Information", expanded=False):
            for i, d in enumerate(docs, 1):
                src = d.metadata.get("source", f"chunk_{i}")
                st.markdown(f"""
                <div class="evidence-box">
                    <strong>📄 Source {i}: {src}</strong>
                    <p>{d.page_content[:300]}...</p>
                </div>
                """, unsafe_allow_html=True)
