import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── Company config ────────────────────────────────────
COMPANY = "NovaPay"
MARKETS = ["UK", "Germany", "India", "UAE", "Singapore", "USA"]
CURRENCIES = ["GBP", "EUR", "INR", "AED", "SGD", "USD"]
MARKET_CURRENCY = dict(zip(MARKETS, CURRENCIES))

CHANNELS = ["Email", "Paid Social", "Organic Search", "Referral", "Webinar", "Influencer"]

CAMPAIGNS = [
    {"name": "Q1 Launch Blitz",     "channel": "Paid Social",    "budget": 18000, "start": "2024-01-10"},
    {"name": "Spring Email Push",   "channel": "Email",          "budget": 6000,  "start": "2024-02-15"},
    {"name": "SEO Content Drive",   "channel": "Organic Search", "budget": 9000,  "start": "2024-03-01"},
    {"name": "Partner Referral Q2", "channel": "Referral",       "budget": 12000, "start": "2024-04-05"},
    {"name": "Fintech Webinar Series","channel": "Webinar",      "budget": 7500,  "start": "2024-05-10"},
    {"name": "Influencer Summer",   "channel": "Influencer",     "budget": 22000, "start": "2024-06-01"},
]

PIPELINE_STAGES = ["Lead", "Qualified", "Demo", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]

# Drop-off rates at each stage (realistic for fintech)
STAGE_CONVERSION = {
    "Lead":        1.00,
    "Qualified":   0.58,
    "Demo":        0.35,
    "Proposal":    0.22,
    "Negotiation": 0.15,
    "Closed Won":  0.09,
    "Closed Lost": 0.06,
}

PRODUCTS = ["NovaPay Basic", "NovaPay Pro", "NovaPay Enterprise"]
PRODUCT_VALUE = {"NovaPay Basic": 299, "NovaPay Pro": 899, "NovaPay Enterprise": 2499}

# ── Helper functions ──────────────────────────────────
def random_date(start_str, days_range=90):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    return start + timedelta(days=random.randint(0, days_range))

def generate_leads(n=1200):
    leads = []
    for i in range(n):
        campaign = random.choice(CAMPAIGNS)
        market = random.choices(
            MARKETS,
            weights=[0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
        )[0]
        product = random.choices(
            PRODUCTS,
            weights=[0.50, 0.35, 0.15]
        )[0]

        # Stage — weighted by conversion rates
        stage = random.choices(
            list(STAGE_CONVERSION.keys()),
            weights=list(STAGE_CONVERSION.values())
        )[0]

        created_date = random_date(campaign["start"], 75)
        
        # Closed Won gets a deal value
        deal_value = 0
        if stage == "Closed Won":
            base = PRODUCT_VALUE[product]
            deal_value = round(base * random.uniform(0.85, 1.30), 2)

        # Email open/click only relevant for email channel
        email_opened = None
        email_clicked = None
        if campaign["channel"] == "Email":
            email_opened = random.random() < 0.42
            email_clicked = email_opened and (random.random() < 0.28)

        leads.append({
            "lead_id":        f"NP-{1000+i}",
            "company":        COMPANY,
            "market":         market,
            "currency":       MARKET_CURRENCY[market],
            "campaign_name":  campaign["name"],
            "channel":        campaign["channel"],
            "campaign_budget":campaign["budget"],
            "product":        product,
            "pipeline_stage": stage,
            "deal_value_usd": deal_value,
            "created_date":   created_date.strftime("%Y-%m-%d"),
            "email_opened":   email_opened,
            "email_clicked":  email_clicked,
            "company_size":   random.choice(["1-10", "11-50", "51-200", "201-500", "500+"]),
            "lead_score":     random.randint(10, 99),
        })
    return pd.DataFrame(leads)

# ── Generate & save ───────────────────────────────────
print("Generating NovaPay CRM data...")
df = generate_leads(1200)

df.to_csv("novapay_crm.csv", index=False)

print(f"✅ Generated {len(df)} leads")
print(f"\nPipeline breakdown:")
print(df['pipeline_stage'].value_counts())
print(f"\nRevenue by market:")
print(df.groupby('market')['deal_value_usd'].sum().sort_values(ascending=False).round(0))
print(f"\nCampaigns:")
print(df['campaign_name'].value_counts())