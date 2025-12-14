# API Setup Guide for TravelGenie

This guide explains how to set up APIs to get better, more comprehensive location information.

## Required API

### 1. Groq API (REQUIRED)
- **Purpose**: AI-powered itinerary generation
- **Get it**: https://console.groq.com/
- **Free tier**: Yes, generous free tier
- **Add to .env**: `GROQ_API_KEY=your_key_here`

## Recommended APIs (For Better Results)

### 2. Foursquare Places API (HIGHLY RECOMMENDED)
- **Purpose**: Detailed information about attractions, restaurants, ratings, addresses
- **Get it**: https://developer.foursquare.com/
- **Free tier**: Yes, 100,000 calls/day free
- **Setup**:
  1. Sign up at Foursquare Developer
  2. Create a new app
  3. Copy your API key
  4. Add to .env: `FOURSQUARE_API_KEY=your_key_here`

### 3. Google Places API (RECOMMENDED)
- **Purpose**: Comprehensive place data, reviews, photos, detailed information
- **Get it**: https://console.cloud.google.com/
- **Free tier**: $200/month credit (usually enough for personal use)
- **Setup**:
  1. Go to Google Cloud Console
  2. Create a project
  3. Enable "Places API"
  4. Create credentials (API Key)
  5. Add to .env: `GOOGLE_PLACES_API_KEY=your_key_here`

### 4. SerpAPI (OPTIONAL)
- **Purpose**: Web search results for comprehensive travel information
- **Get it**: https://serpapi.com/
- **Free tier**: 100 searches/month
- **Setup**:
  1. Sign up at SerpAPI
  2. Get your API key from dashboard
  3. Add to .env: `SERPAPI_KEY=your_key_here`

### 5. OpenTripMap API (OPTIONAL - Fallback)
- **Purpose**: Basic place information (currently used as fallback)
- **Get it**: https://opentripmap.io/docs
- **Free tier**: Yes, 10,000 requests/day
- **Add to .env**: `OPENTRIPMAP_KEY=your_key_here`

## Free Option (No API Key Needed)

### Wikipedia API
- **Purpose**: City overviews and general information
- **Status**: ✅ Always available, no setup needed
- **Note**: Automatically used by the app

## .env File Example

Create a `.env` file in the `WanderGuide` directory:

```env
# Required
GROQ_API_KEY=gsk_your_groq_key_here

# Recommended for better results
FOURSQUARE_API_KEY=your_foursquare_key_here
GOOGLE_PLACES_API_KEY=your_google_key_here
SERPAPI_KEY=your_serpapi_key_here

# Optional fallback
OPENTRIPMAP_KEY=your_opentripmap_key_here
```

## API Priority

The app uses APIs in this order (best to fallback):
1. **Wikipedia** (always available)
2. **Foursquare** (if key provided - best for detailed place info)
3. **Google Places** (if key provided - comprehensive data)
4. **SerpAPI** (if key provided - web search results)
5. **OpenTripMap** (if key provided - basic fallback)

## Why Multiple APIs?

- **Wikipedia**: Free city overviews
- **Foursquare**: Best for detailed venue information, ratings, addresses
- **Google Places**: Most comprehensive, includes reviews and photos
- **SerpAPI**: Real-time web search for latest information
- **OpenTripMap**: Basic fallback if others fail

The more APIs you configure, the richer and more accurate your travel itineraries will be!

