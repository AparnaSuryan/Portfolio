import os

print("Running ETL Pipeline...")


if not os.path.exists('weather_data/weather_raw.json'):
    print("Extracting weather data...")
    os.system("python extract.py")
else:
    print("Weather data already extracted. Skipping extraction.")


print("Transforming weather data...")
os.system("python transform.py")

print("Loading data into MySQL...")
os.system("python load.py")

print("Pipeline completed!")
