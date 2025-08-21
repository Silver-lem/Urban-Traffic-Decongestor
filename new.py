from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    if request.method == "POST":
        start = request.form["start"]
        destination = request.form["destination"]
        traffic = request.form["traffic"]

        prompt = f"Suggest the best route from {start} to {destination} considering traffic is {traffic}."
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI traffic assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            recommendation = response.choices[0].message.content
        except Exception as e:
            recommendation = f"Error: {e}"

    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
