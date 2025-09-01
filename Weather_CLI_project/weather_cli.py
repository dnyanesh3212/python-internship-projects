#!/usr/bin/env python3
"""
Weather CLI App (Internship Project)
------------------------------------
Features:
- Fetches current weather using OpenWeatherMap API
- Fetches 5-day forecast (3-hour interval)
- Groups forecast by day with clear spacing
- Summarizes daily min/max temperatures
- CLI-based temperature trend visualization
- API key stored in config.json
"""

import requests
import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"

# ----------------- Config Handling -----------------
def load_api_key():
    """Load API key from config.json"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Missing {CONFIG_FILE}. Please create one with your API key:")
        print('{ "api_key": "YOUR_API_KEY_HERE" }')
        exit(1)
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data.get("api_key")

# ----------------- API Calls -----------------
def get_current_weather(city, api_key):
    """Fetch current weather data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"\n🌍 Current Weather in {city.title()} ({data['sys']['country']})")
        print("-" * 50)
        print(f"Temperature : {data['main']['temp']}°C")
        print(f"Feels Like  : {data['main']['feels_like']}°C")
        print(f"Condition   : {data['weather'][0]['description'].title()}")
        print(f"Humidity    : {data['main']['humidity']}%")
        print(f"Wind Speed  : {data['wind']['speed']} m/s")
        return data
    else:
        print("❌ City not found or API error!")
        return None

def get_forecast(city, api_key):
    """Fetch 5-day / 3-hour forecast and display summary + trend."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Forecast data not found or API error!")
        return None

    data = response.json()
    forecasts = data['list']

    print(f"\n📅 5-Day Forecast for {city.title()} (Every 3 Hours)")
    print("-" * 60)

    temps = []
    daily_summary = {}
    last_date = ""

    for forecast in forecasts:
        dt_txt = forecast['dt_txt']
        date, time_str = dt_txt.split(" ")
        temp = forecast['main']['temp']
        desc = forecast['weather'][0]['description'].title()
        temps.append(temp)

        # Print a blank line when a new day starts
        if date != last_date:
            print(f"\n=== {date} ===")
            last_date = date

        # Print forecast entry
        print(f"{time_str} | Temp: {temp:.1f}°C | {desc}")

        # Daily min/max summary
        if date not in daily_summary:
            daily_summary[date] = {"min": temp, "max": temp}
        else:
            daily_summary[date]["min"] = min(daily_summary[date]["min"], temp)
            daily_summary[date]["max"] = max(daily_summary[date]["max"], temp)

    # Print daily summary
    print("\n📊 Daily Min/Max Summary:")
    print("-" * 40)
    for date, vals in daily_summary.items():
        print(f"{date} | Min: {vals['min']:.1f}°C | Max: {vals['max']:.1f}°C")

    # CLI bar visualization
    print("\n🌡️ Temperature Trend (relative scale):")
    max_temp = max(temps)
    min_temp = min(temps)
    for temp in temps:
        bar = "█" * int((temp - min_temp) / (max_temp - min_temp + 0.1) * 40)
        print(f"{temp:5.1f}°C | {bar}")

    return data

# ----------------- Main CLI -----------------
def main():
    api_key = load_api_key()
    print("=" * 50)
    print("        ⛅ Weather CLI App (Internship)        ")
    print("=" * 50)

    while True:
        city = input("\nEnter city name (or 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("👋 Goodbye!")
            break
        if not city:
            print("Please enter a valid city name.")
            continue

        current = get_current_weather(city, api_key)
        if current:
            get_forecast(city, api_key)

        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
