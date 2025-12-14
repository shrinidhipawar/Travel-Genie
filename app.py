import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import requests
import pandas as pd
from fpdf import FPDF
from gtts import gTTS
import base64
import io
import folium
from streamlit_folium import st_folium
import sqlite3
from datetime import datetime

load_dotenv()

# --- CONFIG ---
PERSIST_DIR = "chroma_db"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

CITY_NAMES = [
    "hyderabad", "paris", "rome", "london", "bangalore",
    "mumbai", "delhi", "goa", "jaipur", "kolkata"
]

if not GROQ_KEY or not GEOAPIFY_KEY:
    st.error("Missing API keys in .env!")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# --- SESSION STATE INITIALIZATION ---
if "destinations" not in st.session_state:
    st.session_state.destinations = []
if "itinerary_result" not in st.session_state:
    st.session_state.itinerary_result = None
if "itinerary_city" not in st.session_state:
    st.session_state.itinerary_city = None
if "itinerary_mode" not in st.session_state:
    st.session_state.itinerary_mode = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "gallery_index" not in st.session_state:
    st.session_state.gallery_index = 0

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('trips.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS saved_trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            days INTEGER,
            budget TEXT,
            itinerary_text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_trip(city, country, days, budget, text):
    try:
        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO saved_trips (city, country, days, budget, itinerary_text, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                  (city, country, days, budget, text, created_at))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving trip: {e}")
        return False

def get_saved_trips():
    try:
        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('SELECT id, city, country, days, budget, created_at FROM saved_trips ORDER BY created_at DESC')
        trips = c.fetchall()
        conn.close()
        return trips
    except:
        return []

def load_trip(trip_id):
    try:
        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('SELECT itinerary_text, city FROM saved_trips WHERE id = ?', (trip_id,))
        result = c.fetchone()
        conn.close()
        return result
    except:
        return None

def delete_trip(trip_id):
    try:
        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('DELETE FROM saved_trips WHERE id = ?', (trip_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="TravelGenie – AI Trip Planner",
    page_icon=None,
    layout="wide"
)

# --- PREMIUM MODERN CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
    color: #2e2e2e; /* Force dark text for light theme */
}

.stApp {
    background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.9)), url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1");
    background-attachment: fixed;
    background-size: cover;
    background-position: center;
}

h1, h2, h3, h4, h5, h6, span, div, p, li, label {
    color: #2e2e2e;
}

/* HERO */
.hero {
    height: 420px;
    background-image: url("https://images.unsplash.com/photo-1501785888041-af3ef285b470");
    background-size: cover;
    background-position: center;
    border-radius: 0 0 30px 30px;
    margin-bottom: 40px;
}

.hero-overlay {
    background: linear-gradient(rgba(0,0,0,.55), rgba(0,0,0,.7));
    height: 100%;
    padding: 80px;
    color: white;
}

.hero-overlay h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.6rem;
    color: white !important;
}

.hero-overlay p {
    font-size: 1.2rem;
    opacity: 0.9;
    color: white !important;
}

/* SEARCH */
.block {
    max-width: 850px;
    margin: auto;
}

/* RESULT */
.result-wrapper {
    background: white;
    padding: 45px;
    border-radius: 26px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.1);
    margin-top: 40px;
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.result-content {
    font-size: 1.08rem;
    line-height: 1.75;
}

/* BADGES */
.badge {
    padding: 6px 16px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.75rem;
}
.badge-local { background: #e0f2fe; color: #0369a1; }
.badge-api { background: #fdf2f8; color: #9d174d; }
/* BUTTON STYLING */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem;
}

/* Primary Button (Plan Trip) */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box_shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(118, 75, 162, 0.6);
}

/* API Status Badges */
.api-active { color: #10b981; font-weight: bold; }
.api-missing { color: #ef4444; font-weight: bold; }
.api-optional { color: #f59e0b; font-weight: bold; }

</style>
""", unsafe_allow_html=True)




# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="hero-overlay">
        <h1>TravelGenie</h1>
        <p>Curated journeys, designed by AI</p>
    </div>
</div>
""", unsafe_allow_html=True)





# ---------------- SIDEBAR - API & SAVED TRIPS ----------------
with st.sidebar:
    st.markdown("### 📂 Saved Trips")
    saved_trips = get_saved_trips()
    if saved_trips:
        for trip in saved_trips:
            trip_id, city, country, t_days, t_budget, created_at = trip
            with st.expander(f"{city} ({t_days} Days)"):
                st.caption(f"📅 {created_at} | 💰 {t_budget}")
                col_load, col_del = st.columns(2)
                with col_load:
                    if st.button("📂 Load", key=f"load_{trip_id}", use_container_width=True):
                        trip_data = load_trip(trip_id)
                        if trip_data:
                            st.session_state.itinerary_result = trip_data[0]
                            st.session_state.itinerary_city = trip_data[1]
                            st.session_state.itinerary_mode = "SAVED"
                            st.rerun()
                with col_del:
                    if st.button("❌ Delete", key=f"del_{trip_id}", use_container_width=True):
                        delete_trip(trip_id)
                        st.rerun()
    else:
        st.info("No saved trips yet. Plan a trip and click 'Save'!")

    st.markdown("---")

# ---------------- INPUT & MULTI-CITY LOGIC ----------------
from cities import ALL_CITIES


# Popular Destinations for Auto-Suggest
POPULAR_DESTINATIONS = ALL_CITIES

st.markdown("### 🗺️ Plan Your Journey")

# Display Current Route
if st.session_state.destinations:
    st.markdown("#### Current Route:")
    for i, stop in enumerate(st.session_state.destinations):
        st.markdown(f"**{i+1}. {stop['city']}** ({stop['days']} Days)")
    
    if st.button("❌ Clear Route"):
        st.session_state.destinations = []
        st.rerun()
    st.markdown("---")

col1, col2, col3, col4 = st.columns([1.5, 0.6, 0.8, 1])

with col1:
    dest_selection = st.selectbox("Destination", POPULAR_DESTINATIONS, index=0)
    current_city = ""
    current_country = ""
    
    if dest_selection == "Other":
        custom_dest = st.text_input("Enter Destination", placeholder="City, Country")
        if "," in custom_dest:
            current_city = custom_dest.split(",")[0].strip()
            current_country = custom_dest.split(",")[1].strip()
        else:
            current_city = custom_dest.strip()
    else:
        if "," in dest_selection:
            current_city = dest_selection.split(",")[0].strip()
            current_country = dest_selection.split(",")[1].strip()
        else:
            current_city = dest_selection

with col2:
    days = st.number_input("Days", min_value=1, max_value=60, value=3)

with col3:
    start_date = st.date_input("Start Date")

with col4:
    budget = st.selectbox("Budget", ["Budget", "Standard", "Luxury", "Ultra-Luxury"])

# Add Destination / Plan Trip Logic
col_add, col_plan = st.columns([1, 1])

with col_add:
    if st.button("➕ Add Destination"):
        if current_city:
            st.session_state.destinations.append({
                "city": current_city,
                "country": current_country,
                "days": days
            })
            st.success(f"Added {current_city} to route!")
            st.rerun()

with col_plan:
    # Logic to decide what to plan
    # If a route exists, we offer two options to avoid confusion
    if st.session_state.destinations:
        # Multi-City Option
        if st.button(f"Plan Multi-City Trip ({len(st.session_state.destinations)} stops)", type="primary", use_container_width=True):
            st.session_state.planning_mode = "MULTI"
            st.rerun()
            
        # Single City Option Override
        if st.button(f"Plan Only {current_city}", use_container_width=True):
             st.session_state.planning_mode = "SINGLE"
             st.rerun()
    else:
        # Default Single Trip
        if st.button("Plan Trip", type="primary", use_container_width=True):
            st.session_state.planning_mode = "SINGLE"
            st.rerun()

# --- ADVANCED OPTIONS ---
with st.expander("🍽️ Dining Preferences"):
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        dietary = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Halal", "Gluten-Free", "Kosher"])
    with d_col2:
        cuisine_style = st.selectbox("Dining Style", ["Any", "Street Food", "Casual Dining", "Fine Dining", "Michelin Star"])
    
    min_rating = st.slider("Minimum Rating", 3.0, 5.0, 4.0, 0.1)

st.write("")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- API HELPERS ----------------


def fetch_from_wikipedia(city: str) -> str:
    """Fetch comprehensive city information from Wikipedia (FREE, no API key needed)"""
    try:
        # Get city summary from Wikipedia
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + city.replace(" ", "_")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            info = f"City: {data.get('title', city)}\n"
            if 'extract' in data:
                info += f"Overview: {data['extract']}\n"
            if 'coordinates' in data:
                info += f"Coordinates: {data['coordinates'].get('lat')}, {data['coordinates'].get('lon')}\n"
            return info
    except Exception as e:
        pass
    return ""

def fetch_from_foursquare(city: str, query_type: str = "tourist_attraction", limit: int = 15) -> str:
    """Fetch detailed places from Foursquare API (requires API key)"""
    if not FOURSQUARE_API_KEY:
        return ""
    
    try:
        # First, get coordinates for the city
        geo_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={OPENTRIPMAP_KEY}" if OPENTRIPMAP_KEY else None
        if not geo_url:
            # Fallback: use a simple geocoding
            return ""
        
        geo_r = requests.get(geo_url, timeout=5).json()
        lat, lon = geo_r.get("lat"), geo_r.get("lon")
        
        if not lat or not lon:
            return ""
        
        # Foursquare Places API v3
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Accept": "application/json",
            "Authorization": FOURSQUARE_API_KEY
        }
        params = {
            "query": query_type,
            "ll": f"{lat},{lon}",
            "radius": 10000,
            "limit": limit,
            "fields": "name,location,rating,price,description,tips,categories"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            places_info = []
            
            for place in data.get("results", [])[:limit]:
                name = place.get("name", "Unknown")
                location = place.get("location", {})
                address = location.get("formatted_address", location.get("address", ""))
                rating = place.get("rating", "N/A")
                price = place.get("price", "")
                categories = ", ".join([cat.get("name", "") for cat in place.get("categories", [])[:2]])
                
                place_str = f"📍 {name}"
                if categories:
                    place_str += f" ({categories})"
                if address:
                    place_str += f"\n   Address: {address}"
                if rating != "N/A":
                    place_str += f"\n   Rating: {rating}/10"
                if price:
                    place_str += f"\n   Price Level: {'$' * price}"
                
                places_info.append(place_str)
            
            return "\n\n".join(places_info) if places_info else ""
    except Exception as e:
        pass
    return ""

def fetch_from_google_places(city: str, query: str = "", limit: int = 15) -> str:
    """Fetch places from Google Places API (requires API key)"""
    if not GOOGLE_PLACES_API_KEY:
        return ""
    
    try:
        # Text search for places in the city
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{query} in {city}" if query else f"tourist attractions in {city}",
            "key": GOOGLE_PLACES_API_KEY,
            "type": "tourist_attraction"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            places_info = []
            
            for place in data.get("results", [])[:limit]:
                name = place.get("name", "Unknown")
                rating = place.get("rating", "N/A")
                address = place.get("formatted_address", "")
                types = ", ".join([t.replace("_", " ").title() for t in place.get("types", [])[:3]])
                
                place_str = f"📍 {name}"
                if types:
                    place_str += f" ({types})"
                if address:
                    place_str += f"\n   Address: {address}"
                if rating != "N/A":
                    place_str += f"\n   Rating: {rating}/5.0"
                
                places_info.append(place_str)
            
            return "\n\n".join(places_info) if places_info else ""
    except Exception as e:
        pass
    return ""

def fetch_from_serpapi(city: str, query: str) -> str:
    """Fetch comprehensive search results from SerpAPI (requires API key)"""
    if not SERPAPI_KEY:
        return ""
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": f"{query} {city} travel guide attractions restaurants",
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # Extract organic results
            for result in data.get("organic_results", [])[:10]:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                if title and snippet:
                    results.append(f"📌 {title}\n   {snippet}")
            
            return "\n\n".join(results) if results else ""
    except Exception as e:
        pass
    return ""


@st.cache_data
def get_geoapify_places(city: str, api_key: str, limit: int = 20):
    """Fetch raw places data including coordinates"""
    if not api_key:
        return []
    
    try:
        categories = "tourism.attraction,tourism.sights,entertainment.museum,heritage,catering.restaurant"
        geocode_url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={GEOAPIFY_KEY}"
        geo_response = requests.get(geocode_url, timeout=5).json()
        
        if not geo_response.get('features'):
            return []
            
        coords = geo_response['features'][0]['geometry']['coordinates']
        lon, lat = coords[0], coords[1]
        
        places_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},5000&limit={limit}&apiKey={GEOAPIFY_KEY}"
        places_response = requests.get(places_url, timeout=5).json()
        
        results = []
        for feature in places_response.get('features', []):
            props = feature.get('properties', {})
            results.append({
                "name": props.get('name', 'Unknown'),
                "lat": feature['geometry']['coordinates'][1],
                "lon": feature['geometry']['coordinates'][0],
                "categories": props.get('categories', []),
                "address": props.get('formatted', '')
            })
        return results
    except Exception as e:
        st.error(f"Geoapify API Error: {str(e)}")
        # print(f"Geoapify Error: {e}") # Print to console as well
        return []

def fetch_from_geoapify(city: str, limit: int = 15) -> str:
    """Fetch formatted string for LLM context"""
    places = get_geoapify_places(city, GEOAPIFY_KEY, limit)
    if not places:
        return ""
        
    formatted_places = []
    for p in places:
        info = f"📍 {p['name']}"
        if p['categories']:
            info += f" ({', '.join(p['categories'][:2])})"
        if p['address']:
            info += f"\n   {p['address']}"
        formatted_places.append(info)
        
    return "\n\n".join(formatted_places)




# ---------------- MEDIA HELPERS ----------------
def create_pdf(itinerary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Handle unicode by replacing common non-ascii chars or using a compatible font
    # For simplicity, we'll encode/decode to latin-1 and ignore errors
    text = itinerary_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1') 

def create_audio(text):
    # gTTS expects text. limit length to first 500 chars for speed in demo
    short_text = text[:1000] # Limit for demo performance
    tts = gTTS(short_text, lang='en')
    with io.BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)
        return f.read()


def fetch_comprehensive_location_data(city: str, query: str) -> str:
    """Fetch comprehensive location data using multiple APIs"""
    all_data = []
    
    # 1. Wikipedia (always available, free)
    wiki_info = fetch_from_wikipedia(city)
    if wiki_info:
        all_data.append(f"=== CITY OVERVIEW (Wikipedia) ===\n{wiki_info}\n")
    
    # 2. Foursquare (if available)
    foursquare_info = fetch_from_foursquare(city, limit=20)
    if foursquare_info:
        all_data.append(f"=== TOP ATTRACTIONS & PLACES (Foursquare) ===\n{foursquare_info}\n")
    
    # 3. Google Places (if available)
    google_info = fetch_from_google_places(city, query, limit=15)
    if google_info:
        all_data.append(f"=== PLACES OF INTEREST (Google Places) ===\n{google_info}\n")
    
    # 4. SerpAPI (if available) - comprehensive web search
    serp_info = fetch_from_serpapi(city, query)
    if serp_info:
        all_data.append(f"=== ADDITIONAL INFORMATION (Web Search) ===\n{serp_info}\n")
    
    # 5. Fallback to Geoapify if nothing else works
    geoapify_info = fetch_from_geoapify(city)
    if geoapify_info:
        all_data.append(f"=== PLACES (Geoapify) ===\n{geoapify_info}\n")
    
    return "\n".join(all_data) if all_data else "Limited information available. Consider adding API keys for better results."


# ---------------- MAIN LOGIC & STATE MANAGEMENT ----------------
temp = 0.4
top_k = 5

if "planning_mode" not in st.session_state:
    st.session_state.planning_mode = None

# Trigger logic based on planning mode
if st.session_state.planning_mode:
    mode_trigger = st.session_state.planning_mode
    st.session_state.planning_mode = None # Reset immediately so it doesn't loop
    
    # DETERMINE DESTINATIONS
    trips_to_plan = []
    
    if mode_trigger == "MULTI" and st.session_state.destinations:
        trips_to_plan = st.session_state.destinations
    elif mode_trigger == "SINGLE" and current_city: 
        trips_to_plan = [{"city": current_city, "country": current_country, "days": days}]
        # If user explicitly chose single, we might want to clear the old route or just ignore it.
        # Let's just ignore it for this generation.
        
    if not trips_to_plan:
        st.warning("Please select a City and Country or Add a Destination!")
        # st.stop() # Only stop if we really can't proceed, but here we just show warning and let UI render
    
    else:
        with st.spinner(f"Planning your journey to {len(trips_to_plan)} destinations..."):
            # BUILD CONTEXT for ALL cities
            full_context = ""
            full_query_parts = []
            target_city = trips_to_plan[0]['city'] # For slideshow focus
        
            # Prepare filters
            diet_str = f"Dietary: {', '.join(dietary)}" if dietary else ""
            style_str = f"Style: {cuisine_style}" if cuisine_style != "Any" else ""
            rating_str = f"Min Rating: {min_rating}"
            filter_str = f"{diet_str} {style_str} {rating_str}"

            for stop in trips_to_plan:
                c_city = stop['city']
                c_days = stop['days']
                c_country = stop['country']
                
                # Context Fetching
                context_data = fetch_comprehensive_location_data(c_city, "")
                full_context += f"\n=== {c_city.upper()} DATA ===\n{context_data}\n"
                
                full_query_parts.append(f"- {c_city} ({c_country}): {c_days} days")

            # Construct Master Query
            trip_overview = "\n".join(full_query_parts)
            query = f"""Plan a multi-destination trip starting {start_date}.
Destinations:
{trip_overview}
Budget: {budget}.
Preferences: {filter_str}.

Focus on seamless travel between these cities and {budget} experiences."""

            prompt = f"""
You are TravelGenie, a luxury travel planning expert.
LOCATIONS DATA:
{full_context}

USER REQUEST:
{query}

Create a cohesive itinerary.
Structure:
- **Trip Title** (Markdown H1)
- **Logistics**: Brief travel advice between cities (if multi-city).
- **City-by-City Itinerary**:
  - For each city, provide a day-by-day plan.
  - Include specific restaurants matching: {filter_str}
  - Mention specific prices.
- **Budget Summary**: Total estimated cost.

Use the provided location data strictly for attractions/restaurants.
"""
            # Call LLM
            response = client.chat.completions.create(
                model=DEFAULT_GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are TravelGenie, a luxury travel planning expert."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=temp,
            )

            answer = response.choices[0].message.content
            
            # Save to Session State
            st.session_state.itinerary_result = answer
            st.session_state.itinerary_city = target_city # Primary city for visuals
            st.session_state.itinerary_mode = "GENERATED"
            st.session_state.last_prompt = prompt # Save for refinement
            st.session_state.last_answer = answer # Save for refinement
            st.rerun()


# --- RENDER RESULTS FROM STATE ---
if st.session_state.itinerary_result:
    answer = st.session_state.itinerary_result
    target_city = st.session_state.itinerary_city
    mode = st.session_state.itinerary_mode
    
    badge_label = "Live API"
    badge_style = "badge-api"
    
    if mode == "SAVED":
        badge_label = "💾 Saved Trip"
        badge_style = "badge-local"
        
    badge = f'<span class="badge {badge_style}">{badge_label}</span>'

    # --- RESULT DISPLAY ---
    # Display Highlights (Slideshow)
    # Refined logic: If multi-city, we might want to cycle? For now iterate target_city (first city)
    # --- RESULT DISPLAY ---
    # Header Card
    st.markdown(f"""
    <div class="result-wrapper" style="padding-bottom: 10px; margin-bottom: 20px;">
        <div class="result-header">
            <h2>Your Perfect Trip</h2>
            {badge}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content (Rendered as native Markdown)
    st.markdown(answer)
    
    # Separator
    st.markdown("---")
    
    # --- REFINE PLAN (CHAT) ---
    st.markdown("### 💬 Refine Your Plan")
    with st.expander("Make Changes (AI Chat)", expanded=True):
        user_refinement = st.text_input("Ask for changes (e.g., 'Remove the museum', 'Add a vegan dinner')", key="refine_input")
        if st.button("🔄 Update Itinerary") and user_refinement:
            with st.spinner("Updating your plan..."):
                # We need context. Re-use last prompt if available, or just send previous answer as context.
                # Best approach: Send history [System, User(Original), Assistant(Original), User(Refinement)]
                
                msgs = [
                    {"role": "system", "content": "You are TravelGenie. Modify the itinerary based on user requests."},
                ]
                
                # Try to retrieve original prompt from state
                if "last_prompt" in st.session_state:
                     msgs.append({"role": "user", "content": st.session_state.last_prompt})
                
                if "last_answer" in st.session_state:
                     msgs.append({"role": "assistant", "content": st.session_state.last_answer})
                     
                msgs.append({"role": "user", "content": f"Make this change: {user_refinement}. Keep the rest of the itinerary structure consistent."})
                
                refine_response = client.chat.completions.create(
                    model=DEFAULT_GROQ_MODEL,
                    messages=msgs,
                    max_tokens=2500
                )
                
                new_answer = refine_response.choices[0].message.content
                st.session_state.itinerary_result = new_answer
                st.session_state.last_answer = new_answer # Update history
                st.rerun()

    # --- NEW FEATURES: MAP & EXPORT ---
    st.markdown("### Visual Itinerary (Interactive Map)")
    
    map_points = get_geoapify_places(target_city, GEOAPIFY_KEY)
    
    if map_points:
        try:
            lats = [p['lat'] for p in map_points]
            lons = [p['lon'] for p in map_points]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
            
            for p in map_points:
                popup_html = f"<b>{p['name']}</b><br>{p['categories'][0] if p['categories'] else 'Place'}"
                folium.Marker(
                    [p['lat'], p['lon']], 
                    popup=popup_html,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)
            
            st_folium(m, width=None, height=500)
        except Exception as e:
            st.error(f"Error rendering map: {e}")
    else:
        if not GEOAPIFY_KEY:
            st.warning("⚠️ Map unavailable: Geoapify API Key is missing. Add `GEOAPIFY_API_KEY` to your `.env` file.")
        else:
            st.info(f"Could not find specific locations for map in '{target_city}'.")

    st.markdown("---")
    st.markdown("### Tools")
    
    col_tools1, col_tools2, col_tools3 = st.columns(3)
    
    with col_tools1:
        # Save Trip
        if st.button("💾 Save Trip", use_container_width=True):
            if save_trip(target_city, "", 0, "N/A", answer): # Simplified, ideal to capture actual state
                 st.success("Trip Saved!")
                 st.rerun()

    with col_tools2:
        # 2. PDF
        try:
            pdf_data = create_pdf(answer)
            st.download_button(
                label="Download Itinerary (PDF)",
                data=pdf_data,
                file_name=f"TravelGenie_{target_city}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")

    with col_tools3:
        # 3. Audio
        try:
            st.markdown("**Listen to Plan**")
            audio_data = create_audio(answer)
            st.audio(audio_data, format="audio/mp3")
        except Exception as e:
            st.error(f"Could not generate Audio: {e}")


