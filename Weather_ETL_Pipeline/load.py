import pandas as pd
import mysql.connector
from time import sleep
import os
from dotenv import load_dotenv


load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )


def wait_for_db():
    while True:
        try:
            connection = connect_db()
            if connection.is_connected():
                print("MySQL is connected!")
                connection.close()
                break
        except mysql.connector.Error as err:
            print("Waiting for MySQL to be ready...")
            sleep(2)


def load_data_to_mysql():
    
    df = pd.read_csv("weather_data/weather_data.csv")

    
    connection = connect_db()
    cursor = connection.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(255),
        temperature_celsius FLOAT,
        humidity INT,
        weather_description VARCHAR(255),
        timestamp DATETIME
    )
    """)

    
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO weather_data (city, temperature_celsius, humidity, weather_description, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """, (row['city'], row['temperature_celsius'], row['humidity'], row['weather_description'], row['timestamp']))

    
    connection.commit()
    print("Data loaded successfully into MySQL!")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    wait_for_db()  
    load_data_to_mysql()  
