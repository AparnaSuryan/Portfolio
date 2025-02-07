import pandas as pd
import json
import os


weather_data_folder = "weather_data/"
all_data = []


for filename in os.listdir(weather_data_folder):
    if filename.startswith("weather_") and filename.endswith(".json"):  
        with open(os.path.join(weather_data_folder, filename)) as f:
            raw_data = json.load(f)
            
           
            transformed_data = {
                "city": raw_data["name"],
                "temperature_celsius": round(raw_data["main"]["temp"] - 273.15, 2),
                "humidity": raw_data["main"]["humidity"],
                "weather_description": raw_data["weather"][0]["description"],
                "timestamp": pd.to_datetime(raw_data["dt"], unit='s')
            }
            all_data.append(transformed_data)  


df = pd.DataFrame(all_data)


df.to_csv("weather_data/weather_data.csv", index=False)

print("Data transformed successfully!")
