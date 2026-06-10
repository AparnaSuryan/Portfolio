import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=r'C:\Users\ACER\OnboardIQ\.env')

TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
BASE_URL = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_onboarding_tasks(deal_id, deal_name):
    tasks = [
        "Send welcome email to primary contact",
        "Schedule kickoff call within 3 business days",
        "Assign dedicated CSM",
        "Complete product configuration",
        "Send customer satisfaction survey"
    ]

    for task in tasks:
        payload = {
    "properties": {
        "hs_task_subject": task,
        "hs_task_status": "NOT_STARTED",
        "hs_task_priority": "HIGH",
        "hs_task_type": "TODO",
        "hs_timestamp": "2026-06-10T00:00:00.000Z"
    }
}
        response = requests.post(
            f"{BASE_URL}/crm/v3/objects/tasks",
            headers=HEADERS,
            json=payload
        )
        if response.status_code == 201:
            print(f"Task created: {task}")
        else:
            print(f"Failed to create task: {response.text}")

def log_activity(deal_id, message):
    payload = {
        "properties": {
            "hs_note_body": message
        }
    }
    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/notes",
        headers=HEADERS,
        json=payload
    )
    if response.status_code == 201:
        print(f"Activity logged: {message}")
    else:
        print(f"Failed to log activity: {response.text}")