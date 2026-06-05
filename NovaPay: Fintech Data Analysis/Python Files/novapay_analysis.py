#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from textblob import TextBlob
from config import OPENEXCHANGE_APP_ID, NEWS_API_KEY

plt.rcParams['figure.figsize'] = (11, 5)
sns.set_theme(style="whitegrid")

df = pd.read_csv("novapay_crm.csv")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
df.head()



# Pull live rates from API
response = requests.get(
    "https://openexchangerates.org/api/latest.json",
    params={"app_id": OPENEXCHANGE_APP_ID}
)
rates = response.json()['rates']

print("Live exchange rates (vs USD):")
for currency in ["GBP", "EUR", "INR", "AED", "SGD"]:
    print(f"  {currency}: {rates[currency]}")

# Convert each deal value to local currency
def to_local_currency(row):
    if row['deal_value_usd'] == 0:
        return 0
    currency = row['currency']
    rate = rates.get(currency, 1.0)
    return round(row['deal_value_usd'] * rate, 2)

df['deal_value_local'] = df.apply(to_local_currency, axis=1)

print("\nSample — USD vs local currency:")
print(df[df['deal_value_usd'] > 0][
    ['market','currency','deal_value_usd','deal_value_local']
].head(8).to_string(index=False))


market_local = df[df['deal_value_local'] > 0].groupby(
    ['market','currency']
)['deal_value_local'].sum().reset_index()

market_local.columns = ['Market', 'Currency', 'Local Revenue']
market_local['Local Revenue'] = market_local['Local Revenue'].round(0)

print("Revenue in local currency:")
print(market_local.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(market_local['Market'],
              market_local['Local Revenue'],
              color='#2980b9', edgecolor='white', alpha=0.85)

for bar, row in zip(bars, market_local.itertuples()):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 20,
            f"{row.Currency}\n{row._3:,.0f}",
            ha='center', fontsize=9, fontweight='bold')

ax.set_title("NovaPay Revenue in Local Currency (Live Rates)", fontsize=13, fontweight='bold')
ax.set_ylabel("Local Currency Amount")
plt.tight_layout()
plt.savefig("local_currency_revenue.png", dpi=150)
plt.show()


# Pull live headlines
news_response = requests.get(
    "https://newsapi.org/v2/everything",
    params={
        "q": "fintech payments digital banking",
        "language": "en",
        "pageSize": 20,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
)

articles = news_response.json().get('articles', [])
print(f"Pulled {len(articles)} live headlines\n")

# Score sentiment using TextBlob
news_data = []
for article in articles:
    title = article.get('title', '')
    if not title or title == '[Removed]':
        continue
    blob = TextBlob(title)
    sentiment = blob.sentiment.polarity  # -1 negative to +1 positive
    news_data.append({
        'headline':  title[:80],
        'source':    article['source']['name'],
        'published': article['publishedAt'][:10],
        'sentiment': round(sentiment, 3),
        'tone':      'Positive' if sentiment > 0.05
                     else 'Negative' if sentiment < -0.05
                     else 'Neutral'
    })

news_df = pd.DataFrame(news_data)
print(news_df[['headline','tone','sentiment']].to_string(index=False))



tone_counts = news_df['tone'].value_counts()
avg_sentiment = news_df['sentiment'].mean()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
colors = {'Positive':'#27ae60', 'Neutral':'#f39c12', 'Negative':'#e74c3c'}
pie_colors = [colors[t] for t in tone_counts.index]
axes[0].pie(tone_counts.values,
            labels=tone_counts.index,
            colors=pie_colors,
            autopct='%1.1f%%',
            startangle=140)
axes[0].set_title("Fintech News Sentiment Today", fontsize=12, fontweight='bold')

# Sentiment scores bar
news_sorted = news_df.sort_values('sentiment')
bar_colors = [colors[t] for t in news_sorted['tone']]
axes[1].barh(range(len(news_sorted)),
             news_sorted['sentiment'],
             color=bar_colors, edgecolor='white')
axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')
axes[1].set_yticks(range(len(news_sorted)))
axes[1].set_yticklabels(
    [h[:45]+'...' if len(h)>45 else h for h in news_sorted['headline']],
    fontsize=8
)
axes[1].set_title("Headline Sentiment Scores", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Sentiment (-1 negative → +1 positive)")

plt.suptitle(f"Live Market Sentiment — Avg Score: {avg_sentiment:.3f}",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("news_sentiment.png", dpi=150)
plt.show()

print(f"\nOverall market sentiment: {avg_sentiment:.3f}")
print("Interpretation:", "Positive market conditions" if avg_sentiment > 0
      else "Negative market conditions" if avg_sentiment < 0
      else "Neutral market conditions")



campaign_budgets = {
    "Q1 Launch Blitz":        18000,
    "Spring Email Push":      6000,
    "SEO Content Drive":      9000,
    "Partner Referral Q2":    12000,
    "Fintech Webinar Series": 7500,
    "Influencer Summer":      22000,
}

camp = df.groupby(['campaign_name','channel']).agg(
    total_leads   =('lead_id',        'count'),
    closed_won    =('pipeline_stage', lambda x: (x=='Closed Won').sum()),
    total_revenue =('deal_value_usd', 'sum')
).reset_index()

camp['budget']         = camp['campaign_name'].map(campaign_budgets)
camp['roi_%']          = ((camp['total_revenue'] - camp['budget'])
                           / camp['budget'] * 100).round(1)
camp['cost_per_lead']  = (camp['budget'] / camp['total_leads']).round(2)
camp['conversion_%']   = (camp['closed_won'] / camp['total_leads'] * 100).round(1)
camp['revenue_per_lead'] = (camp['total_revenue'] / camp['total_leads']).round(2)

print(camp[['campaign_name','channel','budget','total_revenue',
            'roi_%','cost_per_lead','conversion_%']]
      .sort_values('roi_%', ascending=False).to_string(index=False))



fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Cost per lead by channel
channel_cpl = camp.sort_values('cost_per_lead')
axes[0].barh(channel_cpl['channel'],
             channel_cpl['cost_per_lead'],
             color='#8e44ad', edgecolor='white', alpha=0.85)
for i, val in enumerate(channel_cpl['cost_per_lead']):
    axes[0].text(val + 0.5, i, f'${val:.0f}', va='center', fontweight='bold')
axes[0].set_title("Cost Per Lead by Channel", fontweight='bold')
axes[0].set_xlabel("Cost ($)")

# Conversion rate by channel
channel_conv = camp.sort_values('conversion_%')
axes[1].barh(channel_conv['channel'],
             channel_conv['conversion_%'],
             color='#16a085', edgecolor='white', alpha=0.85)
for i, val in enumerate(channel_conv['conversion_%']):
    axes[1].text(val + 0.05, i, f'{val}%', va='center', fontweight='bold')
axes[1].set_title("Conversion Rate by Channel", fontweight='bold')
axes[1].set_xlabel("Conversion Rate (%)")

plt.suptitle("NovaPay — Channel Efficiency Analysis", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("channel_efficiency.png", dpi=150)
plt.show()



product_stats = df.groupby('product').agg(
    total_leads  =('lead_id',        'count'),
    closed_won   =('pipeline_stage', lambda x: (x=='Closed Won').sum()),
    total_revenue=('deal_value_usd', 'sum')
).reset_index()

product_stats['conversion_%'] = (
    product_stats['closed_won'] / product_stats['total_leads'] * 100
).round(1)
product_stats['avg_deal_size'] = (
    product_stats['total_revenue'] / product_stats['closed_won'].replace(0,1)
).round(0)

print(product_stats.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(product_stats['product'], product_stats['total_leads'],
            color=['#3498db','#2ecc71','#e74c3c'], edgecolor='white')
axes[0].set_title("Leads by Product", fontweight='bold')
axes[0].set_ylabel("Number of Leads")

axes[1].bar(product_stats['product'], product_stats['avg_deal_size'],
            color=['#3498db','#2ecc71','#e74c3c'], edgecolor='white')
axes[1].set_title("Avg Deal Size by Product", fontweight='bold')
axes[1].set_ylabel("Avg Deal Value (USD)")

plt.suptitle("NovaPay — Product Mix Analysis", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("product_mix.png", dpi=150)
plt.show()




df.to_csv("novapay_enriched.csv", index=False)

# Save sentiment summary for dashboard
news_df.to_csv("novapay_sentiment.csv", index=False)

print("Saved novapay_enriched.csv")
print("Saved novapay_sentiment.csv")
print(f"\nFinal dataset shape: {df.shape}")
print(f"News articles scored: {len(news_df)}")
print(f"Avg market sentiment: {avg_sentiment:.3f}")

