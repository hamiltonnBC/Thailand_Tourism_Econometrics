import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD PRIMARY DATASET
# ==========================================
df_primary = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')

# ==========================================
# 2. LOAD EXCHANGE RATE DATA
# ==========================================

# Load CNY to USD (base rate)
df_cny_usd = pd.read_csv('exchangeRates/chinese_yuan_to_usaAEXCHUS.csv')
df_cny_usd['Year'] = pd.to_datetime(df_cny_usd['observation_date']).dt.year
df_cny_usd = df_cny_usd.rename(columns={'AEXCHUS': 'CNY_per_USD'})
df_cny_usd = df_cny_usd[['Year', 'CNY_per_USD']]

# Load destination currencies per USD (wide format)
df_dest_rates = pd.read_csv('exchangeRates/exchange_data.csv')

# Melt the destination rates from wide to long format
df_dest_long = df_dest_rates.melt(
    id_vars=['Country'],
    var_name='Year',
    value_name='Destination_per_USD'
)

# Convert Year to integer
df_dest_long['Year'] = df_dest_long['Year'].astype(int)

# ==========================================
# 3. MERGE AND CALCULATE CNY PER DESTINATION
# ==========================================

# Merge CNY_per_USD with destination rates
df_rates = df_dest_long.merge(df_cny_usd, on='Year', how='left')

# Calculate CNY per Destination Currency
# Formula: CNY_per_Destination = CNY_per_USD / Destination_per_USD
# 
# Example: If CNY_per_USD = 7.1 and THB_per_USD = 35
# Then CNY_per_THB = 7.1 / 35 = 0.203
# Interpretation: 1 Thai Baht costs 0.203 Chinese Yuan
#
# Special case: USA has Destination_per_USD = 1, so CNY_per_USD / 1 = CNY_per_USD (correct!)

df_rates['exchange_rate'] = df_rates['CNY_per_USD'] / df_rates['Destination_per_USD']

# Keep only the columns we need
df_rates_final = df_rates[['Country', 'Year', 'exchange_rate']]

# ==========================================
# 4. MERGE WITH PRIMARY DATASET
# ==========================================

# Drop the old exchange_rate column
if 'exchange_rate' in df_primary.columns:
    df_primary = df_primary.drop('exchange_rate', axis=1)

# Merge with the new exchange rates
df_merged = df_primary.merge(
    df_rates_final,
    on=['Country', 'Year'],
    how='left'
)

# ==========================================
# 5. SAVE UPDATED DATASET
# ==========================================
output_filename = 'Primary_Dataset_For_Panel_FINAL.csv'
df_merged.to_csv(output_filename, index=False)

print(f"✓ Exchange rates updated successfully!")
print(f"✓ Formula: CNY_per_Destination = CNY_per_USD ÷ Destination_per_USD")
print(f"✓ Higher value = Destination is MORE EXPENSIVE for Chinese tourists")
print(f"✓ Saved to: {output_filename}")

print(f"\nSample data for different countries (2020):")
sample = df_merged[df_merged['Year'] == 2020][['Country', 'Year', 'exchange_rate']].sort_values('Country').head(12)
print(sample.to_string(index=False))

print(f"\nExample interpretation (Thailand 2020):")
thailand_2020 = df_merged[(df_merged['Country'] == 'Thailand') & (df_merged['Year'] == 2020)]
if not thailand_2020.empty:
    rate = thailand_2020['exchange_rate'].values[0]
    print(f"- Exchange rate: {rate:.4f} CNY per THB")
    print(f"- This means 1 Thai Baht costs {rate:.4f} Chinese Yuan")
    print(f"- Or equivalently, 1 Yuan buys {1/rate:.2f} Thai Baht")

print(f"\nExchange rate coverage:")
print(f"Total rows: {len(df_merged)}")
print(f"Rows with exchange rate: {df_merged['exchange_rate'].notna().sum()}")
print(f"Rows missing exchange rate: {df_merged['exchange_rate'].isna().sum()}")
