from dotenv import load_dotenv
import os


load_dotenv()


API_KEY = os.getenv('API_KEY')


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


print(f"Connected to {DB_NAME} at {DB_HOST} on port {DB_PORT}")
