import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def log_event(deal_id, deal_name, deal_amount, status, onboarding_plan, welcome_email):
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ONBOARDING_LOG 
            (DEAL_ID, DEAL_NAME, DEAL_AMOUNT, STATUS, ONBOARDING_PLAN, WELCOME_EMAIL)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (deal_id, deal_name, deal_amount, status, onboarding_plan, welcome_email))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Event logged to Snowflake: {deal_name}")
    except Exception as e:
        print(f"Snowflake error: {e}")