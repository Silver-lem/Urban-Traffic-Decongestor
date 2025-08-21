from flask import Flask, request, jsonify
import openai
import os


# Initialize Flask app
app = Flask(__name__)

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Traffic AI Backend is Running 🚦"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    start = data.get("start", "MG Road")
    destination = data.get("destination", "Indiranagar")
    traffic_info = data.get("traffic", "Heavy congestion on MG Road")
    weather_info = data.get("weather", "Rainy")

    # Create a prompt for the AI
    prompt = f"""
    You are an AI traffic assistant for Bangalore.
    Start: {start}
    Destination: {destination}
    Traffic: {traffic_info}
    Weather: {weather_info}

    Suggest 2 alternate routes and explain them in 2-3 sentences each.
    """

    # Call OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # good for fast prototyping
        messages=[{"role": "user", "content": prompt}]
    )

    ai_text = response.choices[0].message["content"]

    return jsonify({"routes": ai_text})

if __name__ == '__main__':
    app.run(debug=True)
