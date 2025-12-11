import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import requests

load_dotenv()

# --- CONFIG ---
PERSIST_DIR = "chroma_db"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_KEY = os.getenv("GROQ_API_KEY")
OPENTRIPMAP_KEY = os.getenv("OPENTRIPMAP_KEY")

CITY_NAMES = [
    "hyderabad", "paris", "rome", "london", "bangalore",
    "mumbai", "delhi", "goa", "jaipur", "kolkata"
]

if not GROQ_KEY or not OPENTRIPMAP_KEY:
    st.error("Missing API keys in .env!")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="TravelGenie – AI Trip Planner",
    page_icon="✈️",
    layout="wide"
)

# --- PREMIUM MODERN CSS ---
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --primary: #4F46E5;
    --secondary: #7C3AED;
    --accent: #FBCB64;
    --glass: rgba(255,255,255,0.45);
    --glass-border: rgba(255,255,255,0.25);
}

/* GLOBAL */
* { font-family: "Inter"; }
.stApp {
    background: linear-gradient(135deg, #4F46E5, #7C3AED, #FBCB64);
    background-attachment: fixed;
}

/* HERO */
.hero {
    padding: 120px 40px;
    color: white;
    border-radius: 0 0 35px 35px;
    background: 
        linear-gradient(120deg, rgba(0,0,0,0.55), rgba(0,0,0,0.2)),
        url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    text-align: center;
    box-shadow: 0 25px 70px rgba(0,0,0,0.4);
}
.hero h1 {
    font-size: 4rem;
    font-family: "Playfair Display";
    font-weight: 800;
}
.hero p {
    opacity: 0.9;
    font-size: 1.25rem;
}

/* CLEAN INPUT AREA (NO BIG BLOCK) */
.block {
    background: none;
    padding: 20px 0;
    margin-top: 40px;
}

/* INPUT - beautiful modern white/glass */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    font-size: 1.1rem !important;
    color: #222 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

.stTextInput > div > div > input:focus {
    background: white !important;
    border: 1px solid var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(79,70,229,0.25) !important;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    padding: 14px;
    font-size: 1.1rem;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    font-weight: 700;
}

/* RESULT WRAPPER */
.result-wrapper {
    background: rgba(255,255,255,0.55);
    padding: 45px;
    border-radius: 25px;
    margin-top: 50px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
    backdrop-filter: blur(18px);
    animation: fadeInUp 0.7s ease;
}

.result-header {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 25px;
}

.result-header h2 {
    font-family: "Playfair Display";
    font-size: 2.6rem;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.result-content {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #1e1e1e;
}

.result-content h1, .result-content h2, .result-content h3, .result-content h4 {
    color: var(--primary);
    margin-top: 28px;
    margin-bottom: 18px;
}

.result-content h1 { font-size: 2.2rem; border-bottom: 3px solid var(--secondary); padding-bottom: 12px; }
.result-content h2 { font-size: 1.8rem; border-left: 5px solid var(--secondary); padding-left: 15px; }
.result-content h3 { font-size: 1.5rem; }
.result-content h4 { font-size: 1.25rem; font-weight: 700; }

.result-content ul, .result-content ol {
    margin: 20px 0;
    padding-left: 0;
}

.result-content ul li, .result-content ol li {
    margin: 12px 0;
    line-height: 1.8;
    color: #333;
    list-style: none;
}

.result-content ul li:before {
    content: "";
    color: var(--primary);
    font-weight: bold;
    margin-right: 10px;
}

.result-content strong {
    font-size: 1.1rem;
    color: var(--primary);
    font-weight: 700;
}

.result-content em {
    color: var(--secondary);
    font-style: italic;
}

.result-content p {
    margin: 18px 0;
    line-height: 1.85;
}

.result-content blockquote {
    border-left: 4px solid var(--secondary);
    padding-left: 20px;
    margin: 25px 0;
    color: #555;
    font-style: italic;
    background: #f5f7ff;
    padding: 15px 20px;
    border-radius: 8px;
}

/* BADGES */
.badge {
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
}
.badge-local { background: #10B981; }
.badge-api { background: #EC4899; }

/* FADE IN */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>✈️ TravelGenie</h1>
    <p>Luxury AI-Powered Travel Planning</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown("### 🔍 Start Planning Your Journey")
st.write("Enter a city, number of days, and interests. Example: **Paris / 3 days / Cafés, Museums**")

col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Query", placeholder="Rome / 4 days / Food, Art, Nightlife", label_visibility="collapsed")
with col2:
    run_btn = st.button("🚀 Plan Trip")
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- API HELPER ----------------
def fetch_from_opentripmap(city: str, limit: int = 10) -> str:
    try:
        geo_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENTRIPMAP_KEY}"
        geo_r = requests.get(geo_url).json()
        lat, lon = geo_r["lat"], geo_r["lon"]

        radius_url = f"https://api.opentripmap.com/0.1/en/places/radius?apikey={OPENTRIPMAP_KEY}&radius=10000&lon={lon}&lat={lat}&limit={limit}"
        places_r = requests.get(radius_url).json()

        places = [
            f"{p['properties'].get('name')} ({p['properties'].get('kinds')})"
            for p in places_r.get("features", [])
            if p['properties'].get('name')
        ]

        return "\n".join(places) if places else "No places found."
    except Exception as e:
        return str(e)


# ---------------- MAIN LOGIC ----------------
temp = 0.4
top_k = 5

if run_btn and query.strip():
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    query_lower = query.lower()
    city = next((c for c in CITY_NAMES if c in query_lower), None)

    results = db.similarity_search_with_score(query, k=top_k)
    valid_docs = [doc for doc, score in results if score < 0.6]

    if valid_docs:
        context = "\n\n".join([d.page_content for d in valid_docs])
        mode = "LOCAL"
    else:
        context = fetch_from_opentripmap(city or query)
        mode = "LIVE API"

    prompt = f"""
Create an amazing, detailed itinerary: CONTEXT: {context} REQUEST: {query} Include: - Catchy headline - Day-by-day breakdown (Morning/Afternoon/Evening) - Times and durations - Restaurant picks - Budget estimates - Travel tips - Hidden gems Make it luxurious and inspiring!"""

    response = client.chat.completions.create(
        model=DEFAULT_GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are TravelGenie, a luxury travel planning expert."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=temp,
    )

    answer = response.choices[0].message.content

    badge = f'<span class="badge badge-local">Local Data</span>' if mode == "LOCAL" else '<span class="badge badge-api">Live API</span>'

    # --- RESULT DISPLAY ---
    st.markdown(f"""
    <div class="result-wrapper">
        <div class="result-header">
            <h2>✨ Your Perfect Trip</h2>
            {badge}
        </div>
        <div class="result-content">{answer}</div>
    </div>
    """, unsafe_allow_html=True)

elif run_btn:
    st.warning("Please enter a query!")
