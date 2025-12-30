import requests
import matplotlib.pyplot as plt

API_KEY = "06965db6d067b5e731d037d269e04c0f"

# -------------------------------
# USER INPUT
# -------------------------------
cities_input = input("Enter city names (comma separated): ")
CITIES = [city.strip() for city in cities_input.split(",") if city.strip()]

if len(CITIES) < 2:
    print("Please enter at least two cities for comparison.")
    exit()

temperatures = {}
humidities = {}

# -------------------------------
# FETCH DATA
# -------------------------------
for city in CITIES:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temperatures[city] = data["main"]["temp"]
        humidities[city] = data["main"]["humidity"]
    else:
        print(f"⚠️ Could not fetch data for {city}")

# -------------------------------
# CHECK VALID DATA
# -------------------------------
if len(temperatures) < 2:
    print("Not enough valid city data to compare.")
    exit()

# -------------------------------
# ANALYTICS
# -------------------------------
hottest_city = max(temperatures, key=temperatures.get)
most_humid_city = max(humidities, key=humidities.get)

print("\nAnalytics Result:")
print("🔥 Hottest City:", hottest_city)
print("💧 Most Humid City:", most_humid_city)

# -------------------------------
# VISUALIZATION
# -------------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(temperatures.keys(), temperatures.values())
plt.title("Temperature Comparison (°C)")
plt.ylabel("Temperature")

plt.subplot(1, 2, 2)
plt.bar(humidities.keys(), humidities.values())
plt.title("Humidity Comparison (%)")
plt.ylabel("Humidity")

plt.suptitle("User-Driven Multi-City Weather Analytics")
plt.tight_layout()
plt.show()
