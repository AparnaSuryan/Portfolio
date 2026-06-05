import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from textblob import TextBlob
from config import OPENEXCHANGE_APP_ID, NEWS_API_KEY

st.set_page_config(
    page_title="NovaPay Marketing Intelligence",
    page_icon="💳",
    layout="wide"
)

# ── Data loaders ─────────────────────────────────────────────────────────────
@st.cache_data
def load_crm():
    return pd.read_csv("novapay_enriched.csv")

@st.cache_data(ttl=3600)
def get_rates():
    r = requests.get(
        "https://openexchangerates.org/api/latest.json",
        params={"app_id": OPENEXCHANGE_APP_ID}
    )
    return r.json().get("rates", {})

@st.cache_data(ttl=3600)
def get_news():
    r = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": "fintech payments digital banking",
            "language": "en",
            "pageSize": 20,
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY
        }
    )
    articles = r.json().get("articles", [])
    rows = []
    for a in articles:
        title = a.get("title", "")
        if not title or title == "[Removed]":
            continue
        score = TextBlob(title).sentiment.polarity
        rows.append({
            "headline":  title[:90],
            "source":    a["source"]["name"],
            "published": a["publishedAt"][:10],
            "sentiment": round(score, 3),
            "tone":      "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"
        })
    return pd.DataFrame(rows)

df      = load_crm()
rates   = get_rates()
news_df = get_news()

CAMPAIGN_BUDGETS = {
    "Q1 Launch Blitz":        18000,
    "Spring Email Push":      6000,
    "SEO Content Drive":      9000,
    "Partner Referral Q2":    12000,
    "Fintech Webinar Series": 7500,
    "Influencer Summer":      22000,
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://via.placeholder.com/200x60?text=NovaPay", width=180)
st.sidebar.title("Marketing Intelligence")
st.sidebar.markdown("Live data · Refreshes every hour")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "Executive Overview",
    "Funnel Analysis",
    "Campaign Performance",
    "Market & Currency",
    "Live News Sentiment"
])

avg_sentiment = news_df["sentiment"].mean() if not news_df.empty else 0
sentiment_label = "🟢 Positive" if avg_sentiment > 0.05 else "🔴 Negative" if avg_sentiment < -0.05 else "🟡 Neutral"
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Market sentiment:** {sentiment_label}")
st.sidebar.markdown(f"**Score:** {avg_sentiment:.3f}")
st.sidebar.markdown(f"**Live rates:** 1 USD = {rates.get('INR',0):.2f} INR")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Overview":

    st.title("💳 NovaPay — Marketing Intelligence Dashboard")
    st.markdown("##### Real-time CRM · Live exchange rates · Live news sentiment")
    st.markdown("---")

    total_leads   = len(df)
    closed_won    = (df["pipeline_stage"] == "Closed Won").sum()
    total_revenue = df["deal_value_usd"].sum()
    total_budget  = sum(CAMPAIGN_BUDGETS.values())
    overall_roi   = ((total_revenue - total_budget) / total_budget * 100)
    conversion    = closed_won / total_leads * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Leads",     f"{total_leads:,}")
    c2.metric("Closed Won",      f"{closed_won}")
    c3.metric("Conversion Rate", f"{conversion:.1f}%")
    c4.metric("Total Revenue",   f"${total_revenue:,.0f}")
    c5.metric("Overall ROI",     f"{overall_roi:.1f}%",
              delta=f"{overall_roi:.1f}%",
              delta_color="inverse")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Pipeline funnel")
        stage_order = ["Lead","Qualified","Demo","Proposal","Negotiation","Closed Won","Closed Lost"]
        funnel = df["pipeline_stage"].value_counts().reindex(stage_order).dropna()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors  = ["#3498db","#2ecc71","#f39c12","#e67e22","#9b59b6","#27ae60","#e74c3c"]
        ax.bar(funnel.index, funnel.values, color=colors, edgecolor="white")
        for i, v in enumerate(funnel.values):
            ax.text(i, v + 5, str(v), ha="center", fontweight="bold", fontsize=9)
        ax.set_title("Sales Pipeline")
        ax.set_ylabel("Leads")
        plt.xticks(rotation=20, fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Revenue by market (USD)")
        market_rev = df.groupby("market")["deal_value_usd"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(market_rev.index, market_rev.values, color="#2980b9", edgecolor="white", alpha=0.85)
        for i, v in enumerate(market_rev.values):
            ax.text(i, v + 30, f"${v:,.0f}", ha="center", fontsize=8, fontweight="bold")
        ax.set_ylabel("Revenue (USD)")
        ax.set_title("Revenue by Market")
        plt.xticks(rotation=15, fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Key insight")
    st.info(
        "📌 **Email is NovaPay's most efficient channel at $28/lead** — yet receives the "
        "smallest budget ($6,000). Influencer costs $105/lead with only 1.9% conversion. "
        "Reallocating 50% of Influencer budget to Email could double qualified leads."
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FUNNEL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Funnel Analysis":

    st.title("🔽 Funnel Analysis")
    st.markdown("Where are leads dropping off — and what does it cost the business?")
    st.markdown("---")

    stage_order = ["Lead","Qualified","Demo","Proposal","Negotiation","Closed Won"]
    funnel = df["pipeline_stage"].value_counts().reindex(stage_order).dropna()

    # Drop-off table
    dropoffs = []
    stages   = list(funnel.index)
    counts   = list(funnel.values)
    for i in range(1, len(counts)):
        rate = (1 - counts[i]/counts[i-1]) * 100
        dropoffs.append({
            "Transition":   f"{stages[i-1]} → {stages[i]}",
            "Leads In":     counts[i-1],
            "Leads Out":    counts[i],
            "Leads Lost":   counts[i-1] - counts[i],
            "Drop-off %":   round(rate, 1)
        })
    dropoff_df = pd.DataFrame(dropoffs)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Drop-off rate by stage")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ["#e74c3c" if x > 40 else "#e67e22" if x > 25 else "#f1c40f"
                  for x in dropoff_df["Drop-off %"]]
        ax.bar(dropoff_df["Transition"], dropoff_df["Drop-off %"],
               color=colors, edgecolor="white")
        for i, v in enumerate(dropoff_df["Drop-off %"]):
            ax.text(i, v + 0.5, f"{v}%", ha="center", fontweight="bold", fontsize=9)
        ax.set_ylim(0, 80)
        ax.set_ylabel("% Lost")
        plt.xticks(rotation=20, fontsize=7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Funnel drop-off table")
        st.dataframe(
            dropoff_df,
            use_container_width=True
        )

    st.markdown("---")
    st.subheader("Filter funnel by channel")

    channel = st.selectbox("Select channel", ["All"] + df["channel"].unique().tolist())
    filtered = df if channel == "All" else df[df["channel"] == channel]

    funnel_f = filtered["pipeline_stage"].value_counts().reindex(stage_order).fillna(0)
    fig, ax  = plt.subplots(figsize=(10, 4))
    ax.bar(funnel_f.index, funnel_f.values, color="#8e44ad", edgecolor="white", alpha=0.85)
    for i, v in enumerate(funnel_f.values):
        ax.text(i, v + 1, str(int(v)), ha="center", fontweight="bold", fontsize=9)
    ax.set_title(f"Funnel — {channel} channel")
    ax.set_ylabel("Leads")
    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CAMPAIGN PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Campaign Performance":

    st.title("📣 Campaign Performance")
    st.markdown("ROI, cost per lead, and conversion rate across all 6 campaigns.")
    st.markdown("---")

    camp = df.groupby(["campaign_name","channel"]).agg(
        total_leads   =("lead_id",        "count"),
        closed_won    =("pipeline_stage", lambda x: (x=="Closed Won").sum()),
        total_revenue =("deal_value_usd", "sum")
    ).reset_index()
    camp["budget"]           = camp["campaign_name"].map(CAMPAIGN_BUDGETS)
    camp["roi_%"]            = ((camp["total_revenue"] - camp["budget"]) / camp["budget"] * 100).round(1)
    camp["cost_per_lead"]    = (camp["budget"] / camp["total_leads"]).round(2)
    camp["conversion_%"]     = (camp["closed_won"] / camp["total_leads"] * 100).round(1)
    camp["revenue_per_lead"] = (camp["total_revenue"] / camp["total_leads"]).round(2)

    c1, c2, c3 = st.columns(3)
    best    = camp.loc[camp["roi_%"].idxmax()]
    worst   = camp.loc[camp["roi_%"].idxmin()]
    cheapest= camp.loc[camp["cost_per_lead"].idxmin()]
    c1.metric("Best ROI campaign",    best["campaign_name"],    f"{best['roi_%']}%")
    c2.metric("Worst ROI campaign",   worst["campaign_name"],   f"{worst['roi_%']}%")
    c3.metric("Cheapest leads",       cheapest["campaign_name"],f"${cheapest['cost_per_lead']}/lead")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("ROI by campaign")
        roi_sorted = camp.sort_values("roi_%", ascending=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = ["#27ae60" if x > 0 else "#e74c3c" for x in roi_sorted["roi_%"]]
        ax.barh(roi_sorted["campaign_name"], roi_sorted["roi_%"],
                color=colors, edgecolor="white")
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        for bar, val in zip(ax.patches, roi_sorted["roi_%"]):
            ax.text(val + (0.5 if val >= 0 else -0.5),
                    bar.get_y() + bar.get_height()/2,
                    f"{val}%", va="center", fontweight="bold", fontsize=9)
        ax.set_xlabel("ROI (%)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Cost per lead vs conversion rate")
        fig, ax = plt.subplots(figsize=(6, 4))
        scatter = ax.scatter(
            camp["cost_per_lead"],
            camp["conversion_%"],
            s=camp["total_leads"] * 2,
            c=camp["roi_%"],
            cmap="RdYlGn",
            edgecolors="white",
            linewidth=0.5,
            alpha=0.9
        )
        for _, row in camp.iterrows():
            ax.annotate(row["channel"],
                        (row["cost_per_lead"], row["conversion_%"]),
                        textcoords="offset points", xytext=(6, 4), fontsize=8)
        plt.colorbar(scatter, ax=ax, label="ROI %")
        ax.set_xlabel("Cost per Lead ($)")
        ax.set_ylabel("Conversion Rate (%)")
        ax.set_title("Cost vs Conversion (bubble = leads volume)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Full campaign table")
    st.dataframe(
        camp[["campaign_name","channel","budget","total_revenue",
              "roi_%","cost_per_lead","conversion_%"]]
        .sort_values("roi_%", ascending=False),
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MARKET & CURRENCY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Market & Currency":

    st.title("🌍 Market & Currency Analysis")
    st.markdown("Revenue adjusted to local currencies using **live exchange rates**.")
    st.markdown("---")

    MARKETS    = ["UK","Germany","India","UAE","Singapore","USA"]
    CURRENCIES = ["GBP","EUR","INR","AED","SGD","USD"]
    MKT_CCY    = dict(zip(MARKETS, CURRENCIES))

    # Live rates strip
    cols = st.columns(5)
    for col, ccy in zip(cols, ["GBP","EUR","INR","AED","SGD"]):
        col.metric(f"1 USD → {ccy}", f"{rates.get(ccy, 0):.4f}")

    st.markdown("---")

    won = df[df["deal_value_usd"] > 0].copy()
    won["deal_value_local"] = won.apply(
        lambda r: round(r["deal_value_usd"] * rates.get(r["currency"], 1), 2), axis=1
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue in local currency (live rates)")
        market_local = won.groupby(["market","currency"])["deal_value_local"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(market_local["market"], market_local["deal_value_local"],
                      color="#2980b9", edgecolor="white", alpha=0.85)
        for bar, row in zip(bars, market_local.itertuples()):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 200,
                    f"{row.currency}\n{row.deal_value_local:,.0f}",
                    ha="center", fontsize=8, fontweight="bold")
        ax.set_ylabel("Local Currency")
        ax.set_title("Revenue in Local Currency")
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Leads vs revenue by market")
        leads_by_mkt = df.groupby("market")["lead_id"].count()
        rev_by_mkt   = df.groupby("market")["deal_value_usd"].sum()
        fig, ax1 = plt.subplots(figsize=(6, 4))
        ax2 = ax1.twinx()
        x = range(len(leads_by_mkt))
        ax1.bar(x, leads_by_mkt.values, color="#3498db", alpha=0.6, label="Leads")
        ax2.plot(x, rev_by_mkt.reindex(leads_by_mkt.index).values,
                 color="#e74c3c", marker="o", linewidth=2, label="Revenue")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(leads_by_mkt.index, rotation=15, fontsize=8)
        ax1.set_ylabel("Leads", color="#3498db")
        ax2.set_ylabel("Revenue (USD)", color="#e74c3c")
        ax1.set_title("Leads vs Revenue by Market")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Market performance table")
    market_table = df.groupby("market").agg(
        Leads        =("lead_id",        "count"),
        Closed_Won   =("pipeline_stage", lambda x: (x=="Closed Won").sum()),
        Revenue_USD  =("deal_value_usd", "sum")
    ).reset_index()
    market_table["Conversion_%"] = (market_table["Closed_Won"] / market_table["Leads"] * 100).round(1)
    market_table["Currency"]     = market_table["market"].map(MKT_CCY)
    market_table["Live_Rate"]    = market_table["Currency"].apply(lambda c: rates.get(c, 1))
    market_table["Revenue_Local"]= (market_table["Revenue_USD"] * market_table["Live_Rate"]).round(0)
    st.dataframe(market_table.sort_values("Revenue_USD", ascending=False), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — LIVE NEWS SENTIMENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Live News Sentiment":

    st.title("📰 Live Fintech News Sentiment")
    st.markdown("Real-time headlines scored for market sentiment — refreshes every hour.")
    st.markdown("---")

    avg  = news_df["sentiment"].mean() if not news_df.empty else 0
    tone = news_df["tone"].value_counts() if not news_df.empty else pd.Series()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Articles analysed", len(news_df))
    c2.metric("Avg sentiment score", f"{avg:.3f}")
    c3.metric("Positive headlines", tone.get("Positive", 0))
    c4.metric("Negative headlines", tone.get("Negative", 0))

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Sentiment breakdown")
        colors = {"Positive":"#27ae60","Neutral":"#f39c12","Negative":"#e74c3c"}
        pie_colors = [colors[t] for t in tone.index]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(tone.values, labels=tone.index, colors=pie_colors,
               autopct="%1.1f%%", startangle=140)
        ax.set_title(f"Today's Fintech Sentiment\nAvg: {avg:.3f}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Headline scores")
        if not news_df.empty:
            sorted_news = news_df.sort_values("sentiment")
            fig, ax = plt.subplots(figsize=(6, 5))
            bar_colors = [colors[t] for t in sorted_news["tone"]]
            ax.barh(range(len(sorted_news)), sorted_news["sentiment"],
                    color=bar_colors, edgecolor="white")
            ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
            ax.set_yticks(range(len(sorted_news)))
            ax.set_yticklabels(
                [h[:40]+"..." if len(h) > 40 else h for h in sorted_news["headline"]],
                fontsize=7
            )
            ax.set_xlabel("Sentiment score")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    st.markdown("---")
    st.subheader("All headlines")
    st.dataframe(
        news_df[["published","source","headline","tone","sentiment"]]
        .sort_values("sentiment", ascending=False),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("What this means for NovaPay")
    if avg > 0.05:
        st.success(
            "🟢 **Positive market conditions.** Fintech sentiment is favourable today. "
            "Good time to launch campaigns — buyers are in a receptive mindset."
        )
    elif avg < -0.05:
        st.error(
            "🔴 **Negative market conditions.** Caution advised on new spend. "
            "Consider pausing top-of-funnel campaigns until sentiment stabilises."
        )
    else:
        st.warning(
            "🟡 **Neutral market conditions.** No strong signal either way. "
            "Focus budget on retention and bottom-of-funnel conversion rather than new acquisition."
        )
