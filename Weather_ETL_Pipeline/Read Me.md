# Weather Data ETL Pipeline (Python, Docker & MySQL)

Automated ETL pipeline to extract, transform, and load weather data into a MySQL database using Python and Docker.

## Overview

This project builds a scalable, automated system for processing weather data from the OpenWeatherMap API. The pipeline extracts, cleans, and loads data into a MySQL database, with Docker ensuring consistent deployment across environments.

## Key Technologies

- Python: ETL logic and data transformation
- MySQL: Relational database for storing weather data
- Docker & Docker Compose: Containerization and orchestration for scalability


#### ETL Workflow

1. Extract: Retrieve weather data from OpenWeatherMap API (CSV format)
2. Transform: Clean and format data (handle missing values, timestamps)
3. Load: Insert cleaned data into MySQL tables
4. Automate: Schedule the pipeline to run periodically for continuous updates


#### Database Schema

- Database: weather_data
- Table: weather
- Columns: city, temperature_celsius, humidity, weather_description, timestamp

## Analysis & Insights

- Average temperatures per city: Berlin 1.51°C, London 4.37°C, New York 3.32°C, Paris 4.54°C, Tokyo 2.16°C
- Average humidity per city: Berlin 84.5%, London 86%, New York 92%, Paris 75%, Tokyo 39%
- Highest recorded temperature: Paris 4.54°C at 2025-02-06 21:51:11 (Overcast clouds)
- Lowest recorded temperature: Berlin -0.58°C at 2025-02-03 18:56:03 (Clear sky)

## Key Features

- Scalable and automated: Reduces manual intervention and ensures continuous data updates
- Reliable storage: Consistent, accurate weather data stored in MySQL
- Containerized deployment: Easy setup and portability across environments

## How to Run

1. Clone the repository
2. Build the Docker containers using docker-compose up --build
3. Ensure MySQL service is running and configured as per the .env file
4. The ETL pipeline will automatically extract, transform, and load weather data

