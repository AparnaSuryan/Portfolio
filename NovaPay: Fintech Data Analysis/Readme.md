# NovaPay Marketing Intelligence Dashboard

A real-time marketing analytics platform for a fictional fintech company — combining synthetic CRM pipeline data with live API data sources to deliver actionable campaign, funnel, and market insights via an interactive Streamlit dashboard.

> "Most portfolio projects are frozen in time. This one pulls live data — open it right now and the exchange rates and news sentiment are from today."

---

## Business Problem

NovaPay is a mid-size fintech operating across 6 global markets. The marketing team is spending $74,500 across 6 campaigns with no clear view of:

- Which campaigns are generating positive ROI
- Where leads are dropping out of the sales funnel
- How currency fluctuations affect revenue across markets
- What the current news sentiment is in their industry

This dashboard answers all four questions in one place, with live data.

---

## Live Dashboard — 5 Pages

| Page | What it shows |
|---|---|
| Executive Overview | KPIs, pipeline funnel, revenue by market |
| Funnel Analysis | Stage drop-off rates, filterable by channel |
| Campaign Performance | ROI, cost per lead, conversion rate, scatter plot |
| Market & Currency | Live exchange rates, local currency revenue |
| Live News Sentiment | Real headlines scored, market condition recommendation |

---

## Key Findings

| Insight | Detail |
|---|---|
| Best campaign | Spring Email Push — lowest cost per lead at $28 |
| Worst campaign | Q1 Launch Blitz — 95.7% negative ROI |
| Biggest funnel drop | Negotiation → Closed Won — 68.5% of deals lost here |
| Most efficient channel | Email — $28/lead vs Influencer's $105/lead |
| Strongest market | India — highest revenue, strongest INR deal values |
| Best converting channel | Organic Search & Referral — both at 3.4% |
| Today's market sentiment | Slightly positive (0.068) — good conditions for campaigns |

---

## Data Flow

```
┌─────────────────┐   ┌──────────────────────┐   ┌─────────────────┐
│  Synthetic CRM  │   │  Open Exchange Rates  │   │    News API     │
│  generate_data  │   │  openexchangerates.org│   │  newsapi.org    │
│  1,200 leads    │   │  Live · hourly cache  │   │  Live · 20 hdls │
└────────┬────────┘   └──────────┬───────────┘   └────────┬────────┘
         │                       │                         │
         └───────────────────────┼─────────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   Analysis Pipeline    │
                    │  novapay_analysis.ipynb│
                    │  · Currency conversion │
                    │  · TextBlob sentiment  │
                    │  · Campaign ROI calc   │
                    └────────────┬───────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   Streamlit Dashboard  │
                    │       app.py           │
                    │   localhost:8501       │
                    └────────────────────────┘
```

---

## Markets & Currencies

| Market | Currency | Live Rate Used |
|---|---|---|
| India | INR | Yes — live from API |
| UK | GBP | Yes — live from API |
| Singapore | SGD | Yes — live from API |
| UAE | AED | Yes — live from API |
| Germany | EUR | Yes — live from API |
| USA | USD | Baseline |

---

## Project Structure

```
NovaPay/
│
├── app.py                    # Streamlit dashboard (5 pages)
├── generate_data.py          # Synthetic CRM data generator
├── config.py                 # API keys (gitignored)
├── test_apis.py              # API connection test
│
├── novapay_eda.ipynb         # Exploratory data analysis
├── novapay_analysis.ipynb    # Full analysis with live API data
│
├── novapay_crm.csv           # Raw generated CRM data
├── novapay_enriched.csv      # CRM + local currency columns
├── novapay_sentiment.csv     # Scored news headlines
│
└── charts/
    ├── funnel_chart.png
    ├── dropoff_chart.png
    ├── campaign_roi.png
    ├── channel_efficiency.png
    ├── market_revenue.png
    ├── local_currency_revenue.png
    ├── news_sentiment.png
    └── product_mix.png
```

---

## Tech Stack

All free and open source:

| Tool | Purpose |
|---|---|
| Python 3.8 | Core language |
| pandas | Data manipulation |
| matplotlib / seaborn | Visualisation |
| requests | API calls |
| TextBlob | NLP sentiment scoring |
| Streamlit | Interactive dashboard |
| Open Exchange Rates API | Live currency data (free tier) |
| NewsAPI | Live news headlines (free tier) |

---

## How to Run

**1 — Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/novapay-marketing-intelligence
cd novapay-marketing-intelligence
```

**2 — Add your API keys**

Create a `config.py` file (this is gitignored — never committed):
```python
OPENEXCHANGE_APP_ID = "your_key_here"
NEWS_API_KEY = "your_key_here"
```

Get free keys (no credit card needed):
- Open Exchange Rates: https://openexchangerates.org/signup/free
- NewsAPI: https://newsapi.org/register

**3 — Install dependencies**
```bash
pip install pandas matplotlib seaborn requests textblob streamlit
```

**4 — Generate the CRM data**
```bash
python generate_data.py
```

**5 — Run the analysis notebook**

Open `novapay_analysis.ipynb` in Jupyter and run all cells. This pulls live API data and saves enriched CSV files.

**6 — Launch the dashboard**
```bash
streamlit run app.py
```

Dashboard opens at `http://localhost:8501`

---

## Business Recommendations

Based on the full analysis, three actions would meaningfully improve NovaPay's marketing performance:

**1 — Reallocate budget from Influencer to Email**
Email costs $28/lead with 2.8% conversion. Influencer costs $105/lead with 1.9% conversion. Moving 50% of the $22,000 Influencer budget to Email would generate an estimated 392 additional leads at current conversion rates.

**2 — Intervene at the Negotiation stage**
68.5% of deals are lost at Negotiation → Closed Won. This is not a marketing problem — it is a sales process or pricing problem. A structured negotiation playbook or limited-time offer trigger at this stage could recover significant revenue.

**3 — Focus international campaigns on India and UK**
These two markets generate 45% of total revenue despite not having the most leads. They have higher average deal values and should receive disproportionate campaign budget, particularly for NovaPay Enterprise tier.

---

## Dataset

CRM data is synthetically generated using Python — structured to mirror a real Salesforce lead and opportunity export with:
- 1,200 leads across 6 campaigns and 6 markets
- Realistic stage conversion rates based on fintech industry benchmarks
- Product mix (Basic / Pro / Enterprise) with market-appropriate deal values
- Email engagement flags (open rate ~42%, click rate ~28%)

News and exchange rate data is pulled live from public APIs at runtime.

---

*Built as a portfolio project demonstrating: synthetic data generation, live API integration, NLP sentiment analysis, funnel analytics, campaign ROI analysis, multi-currency reporting, and interactive dashboard deployment.*
