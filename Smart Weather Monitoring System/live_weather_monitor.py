import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt

API_KEY = "06965db6d067b5e731d037d269e04c0f"
REFRESH_TIME = 60000  # 60 seconds

refresh_job = None

# -------------------------------
# FETCH WEATHER
# -------------------------------
def fetch_weather():
    global refresh_job

    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("message", "City not found"))
            stop_monitoring()
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        result_label.config(
            text=f"""
City: {city.title()}

Temperature: {temp} °C
Humidity: {humidity} %
Pressure: {pressure} hPa
Wind Speed: {wind} m/s
Last Updated: Live
"""
        )

        plot_graph(temp, humidity, pressure, wind, city)

        # Schedule next refresh
        refresh_job = root.after(REFRESH_TIME, fetch_weather)

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error")
        stop_monitoring()

# -------------------------------
# GRAPH
# -------------------------------
def plot_graph(temp, humidity, pressure, wind, city):
    labels = ["Temp", "Humidity", "Pressure", "Wind"]
    values = [temp, humidity, pressure, wind]

    plt.clf()
    plt.bar(labels, values)
    plt.title(f"Live Weather Monitor - {city.title()}")
    plt.pause(0.1)

# -------------------------------
# CONTROL FUNCTIONS
# -------------------------------
def start_monitoring():
    stop_monitoring()
    fetch_weather()

def stop_monitoring():
    global refresh_job
    if refresh_job:
        root.after_cancel(refresh_job)
        refresh_job = None

# -------------------------------
# GUI SETUP
# -------------------------------
root = tk.Tk()
root.title("Live Weather Monitoring System")
root.geometry("420x460")
root.resizable(False, False)

tk.Label(root, text="Live Weather Monitor", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Enter City Name:").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start Monitoring", bg="green", fg="white",
          command=start_monitoring).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Stop", bg="red", fg="white",
          command=stop_monitoring).grid(row=0, column=1, padx=5)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 10))
result_label.pack(pady=10)

tk.Label(root, text="Auto-refresh every 60 seconds", font=("Arial", 8)).pack(side="bottom", pady=5)

plt.ion()  # Interactive mode for live graph
root.mainloop()
