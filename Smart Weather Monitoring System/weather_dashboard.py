import requests
import matplotlib.pyplot as plt

API_KEY = "06965db6d067b5e731d037d269e04c0f"
CITY = "Delhi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(url)
data = response.json()

# ✅ CHECK API RESPONSE
if response.status_code != 200:
    print("Error fetching data from API")
    print(data)
    exit()

temperature = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
humidity = data["main"]["humidity"]
pressure = data["main"]["pressure"]
wind_speed = data["wind"]["speed"]

labels = ["Temperature (°C)", "Feels Like (°C)", "Humidity (%)", "Pressure (hPa)", "Wind Speed (m/s)"]
values = [temperature, feels_like, humidity, pressure, wind_speed]

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, values)
plt.title(f"Weather Dashboard - {CITY}")
plt.ylabel("Values")
plt.xticks(rotation=20)

for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f"{bar.get_height():.1f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()
