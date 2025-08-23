from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

# Configure the Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_recommendation", methods=["POST"])
def get_recommendation():
    data = request.get_json()
    start = data.get("start")
    destination = data.get("destination")
    status = data.get("status")

    # ---- 1. Get Text Recommendation from Gemini ----
    recommendation_text = ""
    try:
        prompt = f"""
You are an expert GPS navigation assistant. Your task is to provide a clear and concise driving route summary from {start} to {destination}, accounting for {status} traffic.

**RULES:**
- Your entire response MUST be a direct, brief summary of the primary route.
- Do NOT include any disclaimers about real-time traffic, estimates, or lack of information.
- Do NOT use conversational filler like "Here is the route...".
- If the traffic status is vague (e.g., "don't know"), assume normal traffic conditions for your calculation.

**FORMAT:**
- Start with "Primary Route:" followed by the main highways.
- On a new line, start with "Estimated Time:".
- On a new line, start with "Estimated Distance:".
"""
        # --- THIS IS THE CORRECTED LINE ---
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        recommendation_text = response.text
    except Exception as e:
        recommendation_text = f"Error from AI model: {str(e)}"

    # ---- 2. Get Route Coordinates from OpenRouteService ----
    route_geometry = None
    try:
        ors_api_key = os.getenv("ORS_API_KEY")
        
        base_url = "https://api.openrouteservice.org/geocode/search"
        start_req = requests.get(f"{base_url}?api_key={ors_api_key}&text={start}")
        dest_req = requests.get(f"{base_url}?api_key={ors_api_key}&text={destination}")

        start_req.raise_for_status()
        dest_req.raise_for_status()
        
        start_coords = start_req.json()['features'][0]['geometry']['coordinates']
        dest_coords = dest_req.json()['features'][0]['geometry']['coordinates']
        
        headers = {
            'Authorization': ors_api_key,
            'Content-Type': 'application/json; charset=utf-8'
        }
        body = {'coordinates': [start_coords, dest_coords]}
        route_req = requests.post(
            'https://api.openrouteservice.org/v2/directions/driving-car/geojson', 
            headers=headers, 
            json=body
        )
        route_req.raise_for_status()
        route_geometry = route_req.json()['features'][0]['geometry']

    except Exception as e:
        print(f"Could not get route geometry: {str(e)}")
        recommendation_text += "\n\n(Could not retrieve map data.)"

    # ---- 3. Return BOTH text and coordinates to the frontend ----
    return jsonify({
        "recommendation": recommendation_text,
        "geometry": route_geometry
    })

if __name__ == "__main__":
    app.run(debug=True)