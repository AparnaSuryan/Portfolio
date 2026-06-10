import streamlit as st
import snowflake.connector
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_data():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DEAL_ID, DEAL_NAME, DEAL_AMOUNT, STATUS, CREATED_AT FROM ONBOARDING_LOG ORDER BY CREATED_AT DESC")
    rows = cursor.fetchall()
    columns = ['Deal ID', 'Company', 'Amount', 'Status', 'Triggered At']
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)

# --- UI ---
st.set_page_config(page_title="OnboardIQ", page_icon="", layout="wide")

st.title("OnboardIQ Dashboard")
st.caption("Real-time onboarding automation monitor for RevOps teams")

df = get_data()

# Stats row
col1, col2, col3 = st.columns(3)
col1.metric("Total Onboardings", len(df))
col2.metric("Active", len(df[df['Status'] == 'triggered']))
col3.metric("Avg Deal Size", f"${df['Amount'].astype(float).mean():,.0f}" if len(df) > 0 else "$0")

st.divider()

# Main table
st.subheader("Onboarding Log")
st.dataframe(df, use_container_width=True)