import pandas as pd
from sqlalchemy import create_engine

# Load clean data
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

# ---- SNOWFLAKE SCHEMA ----
# Normalize DIM_CUSTOMER into sub-dimensions

# DIM_EDUCATION (sub-dimension)
dim_education = pd.DataFrame({
    'education_id': range(1, df['education'].nunique() + 1),
    'education_level': df['education'].unique()
})

# DIM_MARITAL_STATUS (sub-dimension)
dim_marital = pd.DataFrame({
    'marital_id': range(1, df['marital_status'].nunique() + 1),
    'marital_status': df['marital_status'].unique()
})

# DIM_CUSTOMER (now references education_id and marital_id)
dim_customer_snow = df[['id', 'year_birth', 'age', 
                         'income', 'kidhome', 'teenhome',
                         'education', 'marital_status']].copy()
dim_customer_snow.rename(columns={'id': 'customer_id'}, inplace=True)
dim_customer_snow = dim_customer_snow.merge(
    dim_education, left_on='education', right_on='education_level', how='left'
)
dim_customer_snow = dim_customer_snow.merge(
    dim_marital, left_on='marital_status', right_on='marital_status', how='left'
)
dim_customer_snow = dim_customer_snow[['customer_id', 'year_birth', 'age',
                                        'income', 'kidhome', 'teenhome',
                                        'education_id', 'marital_id']]

# DIM_YEAR (sub-dimension)
dim_year = pd.DataFrame({
    'year_id': range(1, df['dt_customer'].dt.year.nunique() + 1),
    'year': df['dt_customer'].dt.year.unique()
})

# DIM_MONTH (sub-dimension)
dim_month = pd.DataFrame({
    'month_id': range(1, 13),
    'month_number': range(1, 13),
    'month_name': ['January','February','March','April','May','June',
                   'July','August','September','October','November','December'],
    'quarter': [1,1,1,2,2,2,3,3,3,4,4,4]
})

# DIM_DATE (now references year_id and month_id)
dim_date_snow = df[['dt_customer']].drop_duplicates().copy()
dim_date_snow['date_id'] = range(1, len(dim_date_snow) + 1)
dim_date_snow['year'] = dim_date_snow['dt_customer'].dt.year
dim_date_snow['month_number'] = dim_date_snow['dt_customer'].dt.month
dim_date_snow = dim_date_snow.merge(dim_year, on='year', how='left')
dim_date_snow = dim_date_snow.merge(dim_month[['month_id','month_number']], 
                                     on='month_number', how='left')
dim_date_snow = dim_date_snow[['date_id', 'dt_customer', 'year_id', 'month_id']]

# DIM_CAMPAIGN_TYPE (sub-dimension)
dim_campaign_type = pd.DataFrame({
    'type_id': [1, 2],
    'campaign_type': ['Retention', 'Acquisition']
})

# DIM_CAMPAIGN (now references type_id)
dim_campaign_snow = pd.DataFrame({
    'campaign_id': [1, 2, 3, 4, 5],
    'campaign_name': ['Campaign 1', 'Campaign 2', 'Campaign 3',
                      'Campaign 4', 'Campaign 5'],
    'type_id': [1, 2, 1, 2, 1]
})

# FACT_MARKETING (same as before)
fact_marketing = df[['id', 'dt_customer', 'total_spending',
                      'total_purchases', 'total_campaigns_accepted',
                      'mntwines', 'mntfruits', 'mntmeatproducts',
                      'mntfishproducts', 'mntsweetproducts', 'mntgoldprods',
                      'numdealspurchases', 'numwebpurchases',
                      'numcatalogpurchases', 'numstorepurchases',
                      'response', 'complain', 'recency']].copy()
fact_marketing.rename(columns={'id': 'customer_id'}, inplace=True)
fact_marketing = fact_marketing.merge(
    dim_date_snow[['date_id', 'dt_customer']],
    on='dt_customer', how='left'
)
fact_marketing.drop(columns=['dt_customer'], inplace=True)

# ---- LOAD TO POSTGRESQL ----
engine = create_engine(
    'postgresql://postgres:admin123@localhost:5434/marketing_analytics'
)

# Load with snow_ prefix so both schemas exist in same database
dim_education.to_sql('snow_dim_education', engine, if_exists='replace', index=False)
dim_marital.to_sql('snow_dim_marital', engine, if_exists='replace', index=False)
dim_customer_snow.to_sql('snow_dim_customer', engine, if_exists='replace', index=False)
dim_year.to_sql('snow_dim_year', engine, if_exists='replace', index=False)
dim_month.to_sql('snow_dim_month', engine, if_exists='replace', index=False)
dim_date_snow.to_sql('snow_dim_date', engine, if_exists='replace', index=False)
dim_campaign_type.to_sql('snow_dim_campaign_type', engine, if_exists='replace', index=False)
dim_campaign_snow.to_sql('snow_dim_campaign', engine, if_exists='replace', index=False)
fact_marketing.to_sql('snow_fact_marketing', engine, if_exists='replace', index=False)

print("Snow_dim_education:", dim_education.shape)
print("Snow_dim_marital:", dim_marital.shape)
print("Snow_dim_customer:", dim_customer_snow.shape)
print("Snow_dim_year:", dim_year.shape)
print("Snow_dim_month:", dim_month.shape)
print("Snow_dim_date:", dim_date_snow.shape)
print("Snow_dim_campaign_type:", dim_campaign_type.shape)
print("Snow_dim_campaign:", dim_campaign_snow.shape)
print("Snow_fact_marketing:", fact_marketing.shape)
print("Snowflake schema loaded!")