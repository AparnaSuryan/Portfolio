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


df['timestamp'] = pd.to_datetime(df['timestamp'])


plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='timestamp', y='temperature_celsius', hue='city', marker='o')


plt.title('Temperature Trends Over Time for Each City')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.legend(title='City')


plt.tight_layout()
plt.savefig('temperature_trends_over_time.png')
plt.show()


weather_counts = df['weather_description'].value_counts()
print("Weather Description Frequency:")
print(weather_counts)


plt.figure(figsize=(8, 5))
sns.barplot(x=weather_counts.index, y=weather_counts.values, palette='coolwarm')
plt.title('Weather Description Frequency')
plt.xlabel('Weather Description')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('weather_description_frequency.png')
plt.show()


average_temp = df.groupby('city')['temperature_celsius'].mean()
plt.figure(figsize=(10, 6))
average_temp.plot(kind='bar', color='skyblue')
plt.title('Average Temperature per City')
plt.xlabel('City')
plt.ylabel('Temperature (°C)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('average_temperature_per_city.png')
plt.show()

average_humidity = df.groupby('city')['humidity'].mean()
plt.figure(figsize=(10, 6))
average_humidity.plot(kind='bar', color='lightgreen')
plt.title('Average Humidity per City')
plt.xlabel('City')
plt.ylabel('Humidity (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('average_humidity_per_city.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='temperature_celsius', y='humidity', hue='weather_description', palette='viridis')
plt.title('Temperature vs. Humidity')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.grid()
plt.tight_layout()
plt.savefig('temp_vs_humidity.png')
plt.show()


plt.figure(figsize=(8, 8))
weather_counts.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Weather Condition Distribution')
plt.ylabel('')  
plt.tight_layout()
plt.savefig('weather_condition_distribution.png')
plt.show()

connection.close()