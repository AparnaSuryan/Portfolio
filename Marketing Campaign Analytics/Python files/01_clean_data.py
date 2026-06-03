import pandas as pd
from sqlalchemy import create_engine

# Load data
df = pd.read_csv('marketing_campaign.csv', sep=';')

# Clean column names
df.columns = df.columns.str.lower().str.strip()

# Convert date column
df['dt_customer'] = pd.to_datetime(df['dt_customer'])

# Add age column
df['age'] = 2024 - df['year_birth']

# Add total spending column
df['total_spending'] = (df['mntwines'] + df['mntfruits'] + 
                        df['mntmeatproducts'] + df['mntfishproducts'] + 
                        df['mntsweetproducts'] + df['mntgoldprods'])

# Add total purchases column
df['total_purchases'] = (df['numdealspurchases'] + df['numwebpurchases'] + 
                         df['numcatalogpurchases'] + df['numstorepurchases'])

# Add total campaigns accepted
df['total_campaigns_accepted'] = (df['acceptedcmp1'] + df['acceptedcmp2'] + 
                                   df['acceptedcmp3'] + df['acceptedcmp4'] + 
                                   df['acceptedcmp5'])

# Drop nulls
df = df.dropna()

print(df.shape)
print(df.dtypes)
print("Cleaning done!")