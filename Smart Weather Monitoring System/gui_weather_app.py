import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt

API_KEY = "06965db6d067b5e731d037d269e04c0f"

# -------------------------------
# FETCH WEATHER FUNCTION
# -------------------------------
def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("message", "City not found"))
            return

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        # Update Labels
        result_label.config(
            text=f"""
City: {city.title()}

Temperature: {temp} °C
Feels Like: {feels} °C
Humidity: {humidity} %
Pressure: {pressure} hPa
Wind Speed: {wind} m/s
"""
        )

        # Plot Graph
        plot_graph(temp, feels, humidity, pressure, wind, city)

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error. Please check internet connection.")

# -------------------------------
# GRAPH FUNCTION
# -------------------------------
def plot_graph(temp, feels, humidity, pressure, wind, city):
    labels = ["Temp", "Feels", "Humidity", "Pressure", "Wind"]
    values = [temp, feels, humidity, pressure, wind]

    plt.figure(figsize=(7, 4))
    bars = plt.bar(labels, values)
    plt.title(f"Weather Data - {city.title()}")
    plt.ylabel("Values")

    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height(),
                 f"{bar.get_height():.1f}",
                 ha="center", va="bottom")

    plt.tight_layout()
    plt.show()

# -------------------------------
# GUI SETUP
# -------------------------------
root = tk.Tk()
root.title("Smart Weather App")
root.geometry("400x420")
root.resizable(False, False)

tk.Label(root, text="Smart Weather App", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Enter City Name:").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather, bg="#4CAF50", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 10))
result_label.pack(pady=10)

tk.Label(root, text="Powered by OpenWeatherMap", font=("Arial", 8)).pack(side="bottom", pady=5)

root.mainloop()
