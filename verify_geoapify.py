import os
from dotenv import load_dotenv
import requests

load_dotenv()

key = os.getenv("GEOAPIFY_API_KEY")

print(f"--- DIAGNOSTIC SCRIPT ---")
print(f"1. Checking Key...")
if not key:
    print("❌ ERROR: GEOAPIFY_API_KEY not found in .env file.")
    print("Please ensure your .env file has: GEOAPIFY_API_KEY=your_key_here")
    exit(1)
else:
    print(f"✅ Key found: {key[:5]}...{key[-5:]}")

print(f"2. Testing API Connectivity...")
city = "Paris"
url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={key}"

try:
    response = requests.get(url, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('features'):
            print("✅ Geocoding successful!")
            coords = data['features'][0]['geometry']['coordinates']
            print(f"   Coords: {coords}")
            
            # Test Places
            print("3. Testing Places API...")
            categories = "tourism.attraction"
            places_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{coords[0]},{coords[1]},5000&limit=5&apiKey={key}"
            p_resp = requests.get(places_url)
            if p_resp.status_code == 200:
                 p_data = p_resp.json()
                 count = len(p_data.get('features', []))
                 print(f"✅ Places API successful! Found {count} places.")
            else:
                 print(f"❌ Places API failed: {p_resp.status_code} - {p_resp.text}")
        else:
            print("⚠️ Geocoding returned no features (Key might be valid but quota exceeded or weird query?)")
            print(f"Response: {data}")
    elif response.status_code == 401:
        print("❌ Authorization Failed: Invalid API Key.")
    else:
        print(f"❌ API Request failed: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Connection Error: {e}")
