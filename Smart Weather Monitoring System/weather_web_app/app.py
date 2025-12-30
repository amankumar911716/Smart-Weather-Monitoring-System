from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "06965db6d067b5e731d037d269e04c0f"

def get_exact_city(lat, lon):
    try:
        url = (
            "https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json"
            "&zoom=18&addressdetails=1"
        )
        headers = {"User-Agent": "SmartWeatherApp/1.0"}
        data = requests.get(url, headers=headers, timeout=10).json()
        address = data.get("address", {})

        return (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("suburb")
            or address.get("county")
            or "Your Location"
        )
    except:
        return "Your Location"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = []
    hourly = []
    error = None

    city = request.form.get("city")
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    try:
        if lat and lon:
            display_city = get_exact_city(lat, lon)

            current_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            )
            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            )

        elif city:
            display_city = city.title()
            current_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={API_KEY}&units=metric"
            )
            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city}&appid={API_KEY}&units=metric"
            )
        else:
            return render_template("index.html")

        current_data = requests.get(current_url).json()
        if current_data.get("cod") != 200:
            return render_template("index.html", error="City not found")

        weather = {
            "city": display_city,
            "temp": round(current_data["main"]["temp"], 1),
            "humidity": current_data["main"]["humidity"],
            "pressure": current_data["main"]["pressure"],
            "wind": current_data["wind"]["speed"],
            "description": current_data["weather"][0]["description"].title()
        }

        forecast_data = requests.get(forecast_url).json()

        for item in forecast_data["list"][:8]:
            hourly.append({
                "time": item["dt_txt"].split(" ")[1][:5],
                "temp": round(item["main"]["temp"], 1)
            })

        daily = {}
        for item in forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {
                    "date": datetime.strptime(date, "%Y-%m-%d").strftime("%a"),
                    "temp": round(item["main"]["temp"], 1)
                }

        forecast = list(daily.values())[:7]

    except Exception as e:
        print(e)
        error = "Something went wrong"

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        hourly=hourly,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
