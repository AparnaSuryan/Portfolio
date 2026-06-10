from flask import Flask, request, jsonify
from ai_engine import generate_onboarding_plan, generate_welcome_email
from hubspot_client import create_onboarding_tasks
from snowflake_client import log_event

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("Webhook received!")

    # Extract deal details
    properties = data.get('properties', {})
    stage = properties.get('dealstage', {}).get('value', '')
    deal_name = properties.get('dealname', {}).get('value', 'Unknown')
    deal_amount = properties.get('amount', {}).get('value', '0')
    deal_id = data.get('dealId', None)

    if stage == 'closedwon':
        print(f"Deal Won: {deal_name} — triggering onboarding!")

        # Generate AI onboarding plan
        plan = generate_onboarding_plan(deal_name, deal_amount)
        print("\n--- ONBOARDING PLAN ---")
        print(plan)

        # Generate AI welcome email
        email = generate_welcome_email(deal_name, deal_amount)
        print("\n--- WELCOME EMAIL ---")
        print(email)

        # Create tasks in HubSpot
        if deal_id:
            print("\n--- CREATING HUBSPOT TASKS ---")
            create_onboarding_tasks(deal_id, deal_name)

        # Log event to Snowflake
        print("\n--- LOGGING TO SNOWFLAKE ---")
        log_event(deal_id, deal_name, deal_amount, "triggered", plan, email)

        return jsonify({
            "status": "triggered",
            "deal": deal_name,
            "onboarding_plan": plan,
            "welcome_email": email
        }), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)