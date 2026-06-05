#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

plt.rcParams['figure.figsize'] = (11, 5)
sns.set_theme(style="whitegrid")

df = pd.read_csv("novapay_crm.csv")
print("Shape:", df.shape)
df.head()




stage_order = ["Lead","Qualified","Demo","Proposal","Negotiation","Closed Won","Closed Lost"]
funnel = df['pipeline_stage'].value_counts().reindex(stage_order).dropna()

fig, ax = plt.subplots(figsize=(12, 5))
colors = ['#3498db','#2ecc71','#f39c12','#e67e22','#9b59b6','#27ae60','#e74c3c']
bars = ax.bar(funnel.index, funnel.values, color=colors, edgecolor='white', width=0.6)

for bar, val in zip(bars, funnel.values):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 8,
            str(val), ha='center', fontweight='bold', fontsize=11)

ax.set_title("NovaPay — Sales Funnel Pipeline", fontsize=14, fontweight='bold')
ax.set_ylabel("Number of Leads")
ax.set_xlabel("Pipeline Stage")
plt.tight_layout()
plt.savefig("funnel_chart.png", dpi=150)
plt.show()






stages = ["Lead","Qualified","Demo","Proposal","Negotiation","Closed Won"]
counts = [funnel[s] for s in stages]

dropoffs = []
for i in range(1, len(counts)):
    rate = (1 - counts[i]/counts[i-1]) * 100
    dropoffs.append({
        "Transition": f"{stages[i-1]} → {stages[i]}",
        "Leads Lost": counts[i-1] - counts[i],
        "Drop-off %": round(rate, 1)
    })

dropoff_df = pd.DataFrame(dropoffs)
print(dropoff_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 4))
colors = ['#e74c3c' if x > 40 else '#e67e22' if x > 25 else '#f1c40f'
          for x in dropoff_df['Drop-off %']]
bars = ax.bar(dropoff_df['Transition'], dropoff_df['Drop-off %'],
              color=colors, edgecolor='white')
for bar, val in zip(bars, dropoff_df['Drop-off %']):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.5,
            f'{val}%', ha='center', fontweight='bold')
ax.set_title("Drop-off Rate Between Pipeline Stages", fontsize=13, fontweight='bold')
ax.set_ylabel("% of Leads Lost")
ax.set_ylim(0, 65)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("dropoff_chart.png", dpi=150)
plt.show()



campaign_budgets = {
    "Q1 Launch Blitz":       18000,
    "Spring Email Push":     6000,
    "SEO Content Drive":     9000,
    "Partner Referral Q2":   12000,
    "Fintech Webinar Series":7500,
    "Influencer Summer":     22000,
}

campaign_stats = df.groupby('campaign_name').agg(
    total_leads    = ('lead_id', 'count'),
    closed_won     = ('pipeline_stage', lambda x: (x=='Closed Won').sum()),
    total_revenue  = ('deal_value_usd', 'sum')
).reset_index()

campaign_stats['budget'] = campaign_stats['campaign_name'].map(campaign_budgets)
campaign_stats['roi_%'] = ((campaign_stats['total_revenue'] - campaign_stats['budget'])
                            / campaign_stats['budget'] * 100).round(1)
campaign_stats['cost_per_lead'] = (campaign_stats['budget']
                                    / campaign_stats['total_leads']).round(2)
campaign_stats['conversion_%'] = (campaign_stats['closed_won']
                                   / campaign_stats['total_leads'] * 100).round(1)

print(campaign_stats[['campaign_name','budget','total_revenue',
                       'roi_%','cost_per_lead','conversion_%']]
      .sort_values('roi_%', ascending=False).to_string(index=False))



roi_sorted = campaign_stats.sort_values('roi_%', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#27ae60' if x > 0 else '#e74c3c' for x in roi_sorted['roi_%']]
bars = ax.barh(roi_sorted['campaign_name'], roi_sorted['roi_%'],
               color=colors, edgecolor='white')
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
for bar, val in zip(bars, roi_sorted['roi_%']):
    ax.text(val + (1 if val >= 0 else -1),
            bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontweight='bold', fontsize=10)
ax.set_title("Campaign ROI — NovaPay 2024", fontsize=13, fontweight='bold')
ax.set_xlabel("ROI (%)")
plt.tight_layout()
plt.savefig("campaign_roi.png", dpi=150)
plt.show()




market_rev = df.groupby('market')['deal_value_usd'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(market_rev.index, market_rev.values,
              color='#3498db', edgecolor='white', alpha=0.85)
for bar, val in zip(bars, market_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 30,
            f'${val:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax.set_title("Revenue by Market — NovaPay 2024", fontsize=13, fontweight='bold')
ax.set_ylabel("Total Revenue (USD)")
plt.tight_layout()
plt.savefig("market_revenue.png", dpi=150)
plt.show()

