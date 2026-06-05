import requests
from config import OPENEXCHANGE_APP_ID, NEWS_API_KEY

# Test 1 — Exchange Rates
print("Testing Exchange Rates API...")
r1 = requests.get(
    "https://openexchangerates.org/api/latest.json",
    params={"app_id": OPENEXCHANGE_APP_ID}
)
data1 = r1.json()
if "rates" in data1:
    print("✅ Exchange Rates working!")
    print(f"   EUR: {data1['rates']['EUR']}")
    print(f"   GBP: {data1['rates']['GBP']}")
    print(f"   INR: {data1['rates']['INR']}")
else:
    print("❌ Something wrong:", data1)

print()

# Test 2 — News API
print("Testing News API...")
r2 = requests.get(
    "https://newsapi.org/v2/everything",
    params={
        "q": "fintech payments",
        "language": "en",
        "pageSize": 3,
        "apiKey": NEWS_API_KEY
    }
)
data2 = r2.json()
if data2.get("status") == "ok":
    print("✅ News API working!")
    for article in data2["articles"][:3]:
        print(f"   - {article['title'][:60]}...")
else:
    print("❌ Something wrong:", data2)