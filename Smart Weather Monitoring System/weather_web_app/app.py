from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "06965db6d067b5e731d037d269e04c0f"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = {
                    "city": city.title(),
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind": data["wind"]["speed"]
                }
            else:
                error = "City not found or API error"

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

