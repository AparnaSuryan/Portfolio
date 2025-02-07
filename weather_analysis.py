import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


connection = mysql.connector.connect(
    host="db",
    user="username",
    password="password", 
    database="weather_data" 
)


query = "SELECT * FROM weather_data"
df = pd.read_sql(query, connection)


average_temp = df.groupby('city')['temperature_celsius'].mean()
average_humidity = df.groupby('city')['humidity'].mean()

print("Average Temperature per City:")
print(average_temp)

print("\nAverage Humidity per City:")
print(average_humidity)


highest_temp = df.loc[df['temperature_celsius'].idxmax()]
lowest_temp = df.loc[df['temperature_celsius'].idxmin()]

print("\nHighest Temperature Record:")
print(highest_temp)

print("\nLowest Temperature Record:")
print(lowest_temp)


connection.close()
