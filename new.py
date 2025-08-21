from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Load OpenAI client (make sure OPENAI_API_KEY is set in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Route to serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for AJAX requests
@app.route("/get_recommendation", methods=["POST"])
def get_recommendation():
    data = request.get_json()  # get JSON from JS fetch
    start = data.get("start")
    destination = data.get("destination")
    status = data.get("status")

    # --- for testing only ---
    # return a fake response so we know backend works
    return jsonify({
        "recommendation": f"Got your request: {start} → {destination}, traffic = {status}"
    })

if __name__ == "__main__":
    app.run(debug=True)
