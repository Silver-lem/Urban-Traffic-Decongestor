from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
 
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_recommendation", methods=["POST"])
def get_recommendation():
    data = request.get_json()
    start = data.get("start")
    destination = data.get("destination")
    status = data.get("status")

    # ---- 1. Get Text Recommendation from OpenAI ----
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
        response = openai.chat.completions.create(
            model="gpt-4o-mini",   # You can switch to gpt-4o if you want
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        recommendation_text = response.choices[0].message.content.strip()
    except Exception as e:
        recommendation_text = f"Error from AI model: {str(e)}"

    
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

@app.route("/get_events", methods=["GET"])
def get_events():
    try:
        meetup_api_key = os.getenv("MEETUP_API_KEY")
        url = f"https://api.meetup.com/find/upcoming_events?&sign=true&photo-host=public&lon=78.4867&lat=17.3850&radius=20&page=5&key={meetup_api_key}"

        resp = requests.get(url)
        resp.raise_for_status()
        events_data = resp.json()

        events = []
        for e in events_data.get("events", []):
            event_info = {
                "name": e.get("name"),
                "venue": e.get("venue", {}).get("name", "Unknown Venue"),
                "address": e.get("venue", {}).get("address_1", "No address available"),
                "time": e.get("local_date") + " " + e.get("local_time"),
                "lat": e.get("venue", {}).get("lat"),
                "lng": e.get("venue", {}).get("lon")
            }
            events.append(event_info)

        return jsonify({"events": events})

    except Exception as e:
        print("Error fetching events:", str(e))
        return jsonify({"events": []})


if __name__ == "__main__":
    app.run(debug=True)
