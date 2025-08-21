from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def index():
    # Loads our simple HTML page
    return render_template("index.html")

@app.route("/get_recommendation", methods=["POST"])
def get_recommendation():
    try:
        data = request.json
        start = data.get("start")
        destination = data.get("destination")
        traffic = data.get("traffic")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart assistant giving traffic advice."},
                {"role": "user", "content": f"Start: {start}, Destination: {destination}, Traffic: {traffic}. Suggest the best route."}
            ]
        )

        recommendation = response.choices[0].message.content
        return jsonify({"recommendation": recommendation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)