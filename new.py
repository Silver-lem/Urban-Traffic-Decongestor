from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Load OpenAI client (make sure OPENAI_API_KEY is set in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_recommendation", methods=["POST"])
def get_recommendation():
    data = request.get_json()
    start = data.get("start")
    destination = data.get("destination")
    status = data.get("status")

    # Construct prompt
    prompt = f"Suggest the best route from {start} to {destination} considering the traffic is {status}."

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight + cheap
            messages=[
                {"role": "system", "content": "You are a helpful AI traffic assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        recommendation = response.choices[0].message.content

    except Exception as e:
        recommendation = f"Error: {str(e)}"

    return jsonify({"recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
