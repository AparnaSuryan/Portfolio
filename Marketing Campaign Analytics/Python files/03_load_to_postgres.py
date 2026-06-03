import pandas as pd
from sqlalchemy import create_engine

# Load clean data (copy same cleaning code)
df = pd.read_csv('marketing_campaign.csv', sep=';')
df.columns = df.columns.str.lower().str.strip()
df['dt_customer'] = pd.to_datetime(df['dt_customer'])
df['age'] = 2024 - df['year_birth']
df['total_spending'] = (df['mntwines'] + df['mntfruits'] + 
                        df['mntmeatproducts'] + df['mntfishproducts'] + 
                        df['mntsweetproducts'] + df['mntgoldprods'])
df['total_purchases'] = (df['numdealspurchases'] + df['numwebpurchases'] + 
                         df['numcatalogpurchases'] + df['numstorepurchases'])
df['total_campaigns_accepted'] = (df['acceptedcmp1'] + df['acceptedcmp2'] + 
                                   df['acceptedcmp3'] + df['acceptedcmp4'] + 
                                   df['acceptedcmp5'])
df = df.dropna()

# Build star schema tables
dim_customer = df[['id', 'year_birth', 'age', 'education', 
                   'marital_status', 'income', 'kidhome', 
                   'teenhome']].copy()
dim_customer.rename(columns={'id': 'customer_id'}, inplace=True)

dim_date = df[['dt_customer']].copy()
dim_date = dim_date.drop_duplicates()
dim_date['date_id'] = range(1, len(dim_date) + 1)
dim_date['year'] = dim_date['dt_customer'].dt.year
dim_date['month'] = dim_date['dt_customer'].dt.month
dim_date['quarter'] = dim_date['dt_customer'].dt.quarter
dim_date['day_of_week'] = dim_date['dt_customer'].dt.day_name()
dim_date = dim_date[['date_id', 'dt_customer', 'year', 
                      'month', 'quarter', 'day_of_week']]

dim_campaign = pd.DataFrame({
    'campaign_id': [1, 2, 3, 4, 5],
    'campaign_name': ['Campaign 1', 'Campaign 2', 'Campaign 3', 
                      'Campaign 4', 'Campaign 5'],
    'campaign_type': ['Retention', 'Acquisition', 'Retention', 
                      'Acquisition', 'Retention']
})

fact_marketing = df[['id', 'dt_customer', 'total_spending', 
                      'total_purchases', 'total_campaigns_accepted',
                      'mntwines', 'mntfruits', 'mntmeatproducts',
                      'mntfishproducts', 'mntsweetproducts', 'mntgoldprods',
                      'numdealspurchases', 'numwebpurchases',
                      'numcatalogpurchases', 'numstorepurchases',
                      'response', 'complain', 'recency']].copy()
fact_marketing.rename(columns={'id': 'customer_id'}, inplace=True)
fact_marketing = fact_marketing.merge(
    dim_date[['date_id', 'dt_customer']], 
    on='dt_customer', how='left'
)
fact_marketing.drop(columns=['dt_customer'], inplace=True)

# ---- CONNECT TO POSTGRESQL ----
engine = create_engine(
    'postgresql://postgres:admin123@localhost:5434/marketing_analytics'
)

# ---- LOAD TO POSTGRESQL ----
dim_customer.to_sql('dim_customer', engine, if_exists='replace', index=False)
dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)
dim_campaign.to_sql('dim_campaign', engine, if_exists='replace', index=False)
fact_marketing.to_sql('fact_marketing', engine, if_exists='replace', index=False)

print("All tables loaded to PostgreSQL!")