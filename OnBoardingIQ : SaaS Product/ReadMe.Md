# OnboardIQ

> **AI-powered customer onboarding automation for RevOps teams**

OnboardIQ automatically triggers a structured onboarding workflow the moment a deal is marked "Won" in HubSpot — eliminating manual handoff chaos and reducing time-to-value for new customers.

---

## The Problem

When a deal closes, RevOps teams spend 2–4 hours manually:
- Writing welcome emails
- Creating onboarding tasks one by one
- Assigning a CSM via Slack messages that get buried
- Hoping nothing falls through the cracks

**The result:** Delayed onboarding, inconsistent customer experiences, and zero visibility.

---

## The Solution

OnboardIQ listens for "Deal Won" events in HubSpot and instantly:

1. Generates a personalized 4-week onboarding plan using AI
2. Drafts a personalized welcome email using deal data
3. Auto-creates 5 onboarding tasks in HubSpot
4. Logs every event to Snowflake for audit trail
5. Updates the RevOps dashboard in real time

**Time from deal close to onboarding triggered: < 5 seconds.**

---

## Architecture

```
HubSpot CRM (Deal Won)
        ↓
OnboardIQ Engine (Python / Flask)
        ↓              ↓
  Claude API      HubSpot API
  (AI plan +     (tasks + logging)
   email draft)
        ↓
    Snowflake
    (event log)
        ↓
 Streamlit Dashboard
 (RevOps visibility)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| CRM | HubSpot API |
| AI | Claude API (claude-sonnet-4) |
| Data Store | Snowflake |
| Dashboard | Streamlit |

---

## Installation

```bash
git clone https://github.com/yourusername/onboardiq.git
cd onboardiq
pip install flask python-dotenv requests snowflake-connector-python streamlit
```

Create a `.env` file:
```
HUBSPOT_ACCESS_TOKEN=your_hubspot_private_app_token
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ONBOARDIQ
SNOWFLAKE_SCHEMA=EVENTS
```

Run the webhook server:
```bash
python app/webhook.py
```

Run the dashboard:
```bash
python -m streamlit run app/dashboard.py
```

---

## Test It

Simulate a "Deal Won" event:
```bash
curl -X POST http://127.0.0.1:5000/webhook \
  -H "Content-Type: application/json" \
  -d "{\"properties\": {\"dealstage\": {\"value\": \"closedwon\"}, \"dealname\": {\"value\": \"Acme Corp\"}, \"amount\": {\"value\": \"12000\"}}, \"dealId\": \"123456\"}"
```

---

## Project Structure

```
onboardiq/
├── app/
│   ├── webhook.py          # Flask webhook listener
│   ├── ai_engine.py        # AI plan + email generator
│   ├── hubspot_client.py   # HubSpot API integration
│   ├── snowflake_client.py # Snowflake event logging
│   └── dashboard.py        # Streamlit dashboard
├── docs/
│   └── hubspot_schema.md   # HubSpot payload schema
├── .env
├── .gitignore
└── requirements.txt
```

---

## Roadmap

- [ ] Real Claude API integration (when credits available)
- [ ] CSM auto-assignment by capacity rules
- [ ] Slack channel auto-creation per customer
- [ ] Salesforce integration
- [ ] Email open/click tracking
- [ ] Deploy to Render

---

## Links

| Resource | Link |
|---|---|
| Product Requirements Doc (Notion) | [View PRD](https://app.notion.com/p/OnboardIQ-Product-Requirements-Document-PRD-378e614e2374806eb21be3e1526886cc?source=copy_link) |
| Miro Board (User Journey + Architecture) | [View Miro](https://miro.com/app/board/uXjVHI1JTn8=/?share_link_id=822326793031) |
| Trello Sprint Board | [View Trello](https://trello.com/b/7NO3bCQg/onboardiq-product-sprints) |
| Demo Video | [Watch Demo](https://canva.link/nfo6t8hh0tg8cnl) |

---

*Built as a full end-to-end SaaS product - from PRD to working MVP : using Notion, Miro, Trello, HubSpot, Snowflake, and Streamlit.*
