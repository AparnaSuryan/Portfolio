import requests
import json
import os
import csv
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
CITIES = ["Berlin", "Paris", "London", "Newyork", "Tokyo"]  
URL = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"


def fetch_weather():
    
    with open("weather_data/all_weather.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["city", "temperature_celsius", "humidity", "weather_description", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  
        
        
        for city in CITIES:
            response = requests.get(URL.format(city=city, API_KEY=API_KEY))
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": city,
                    "temperature_celsius": data["main"]["temp"] - 273.15,  
                    "humidity": data["main"]["humidity"],
                    "weather_description": data["weather"][0]["description"],
                    "timestamp": data["dt"]
                }
                writer.writerow(weather)  
                print(f"Data for {city} extracted successfully!")
            else:
                print(f"Failed to fetch data for {city}: {response.status_code}")

if __name__ == "__main__":
    fetch_weather()
