def generate_onboarding_plan(deal_name, deal_amount):
    # MOCK: Replace this with real Claude API call when you have credits
    plan = f"""
    ONBOARDING PLAN FOR {deal_name.upper()}
    =========================================
    Deal Value: ${deal_amount}

    Week 1 — Setup & Kickoff
    - Send welcome email to primary contact
    - Schedule kickoff call within 3 business days
    - Create account in internal systems

    Week 2 — Product Setup
    - Complete product configuration
    - Assign dedicated CSM
    - Share onboarding documentation

    Week 3 — Training
    - Run product walkthrough session
    - Share training materials
    - Set up weekly check-in cadence

    Week 4 — Go Live
    - Confirm all setup tasks complete
    - Hand off to CSM for ongoing support
    - Send customer satisfaction survey
    """
    return plan


def generate_welcome_email(deal_name, deal_amount):
    # MOCK: Replace this with real Claude API call when you have credits
    email = f"""
    Subject: Welcome to OnboardIQ, {deal_name}!

    Hi there,

    We're thrilled to have {deal_name} on board!

    Your account is now active and your dedicated Customer 
    Success Manager will be reaching out within 24 hours 
    to schedule your kickoff call.

    Deal summary:
    - Account: {deal_name}
    - Investment: ${deal_amount}
    - Onboarding start: Today

    Looking forward to working with you!

    The OnboardIQ Team
    """
    return email