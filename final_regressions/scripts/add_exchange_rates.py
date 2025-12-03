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
df_cny_usd = df_cny_usd.rename(columns={'AEXCHUS': 'CNY_to_USD'})
df_cny_usd = df_cny_usd[['Year', 'CNY_to_USD']]

# Load other exchange rates (all are USD to local currency)
df_usd_jpy = pd.read_csv('exchangeRates/Japan_USA_AEXJPUS.csv')
df_usd_jpy['Year'] = pd.to_datetime(df_usd_jpy['observation_date']).dt.year
df_usd_jpy = df_usd_jpy.rename(columns={'AEXJPUS': 'USD_to_JPY'})
df_usd_jpy = df_usd_jpy[['Year', 'USD_to_JPY']]

df_usd_krw = pd.read_csv('exchangeRates/Korean_won_to_usa_AEXKOUS.csv')
df_usd_krw['Year'] = pd.to_datetime(df_usd_krw['observation_date']).dt.year
df_usd_krw = df_usd_krw.rename(columns={'AEXKOUS': 'USD_to_KRW'})
df_usd_krw = df_usd_krw[['Year', 'USD_to_KRW']]

df_usd_myr = pd.read_csv('exchangeRates/malaysian_to_USA_dollar_AEXMAUS.csv')
df_usd_myr['Year'] = pd.to_datetime(df_usd_myr['observation_date']).dt.year
df_usd_myr = df_usd_myr.rename(columns={'AEXMAUS': 'USD_to_MYR'})
df_usd_myr = df_usd_myr[['Year', 'USD_to_MYR']]

df_usd_sgd = pd.read_csv('exchangeRates/singapore_to_USA_AEXSIUS.csv')
df_usd_sgd['Year'] = pd.to_datetime(df_usd_sgd['observation_date']).dt.year
df_usd_sgd = df_usd_sgd.rename(columns={'AEXSIUS': 'USD_to_SGD'})
df_usd_sgd = df_usd_sgd[['Year', 'USD_to_SGD']]

df_usd_aud = pd.read_csv('exchangeRates/USA_To_Australia_AEXUSAL.csv')
df_usd_aud['Year'] = pd.to_datetime(df_usd_aud['observation_date']).dt.year
df_usd_aud = df_usd_aud.rename(columns={'AEXUSAL': 'USD_to_AUD'})
df_usd_aud = df_usd_aud[['Year', 'USD_to_AUD']]

df_usd_gbp = pd.read_csv('exchangeRates/USA_to_UK_AEXUSUK.csv')
df_usd_gbp['Year'] = pd.to_datetime(df_usd_gbp['observation_date']).dt.year
df_usd_gbp = df_usd_gbp.rename(columns={'AEXUSUK': 'USD_to_GBP'})
df_usd_gbp = df_usd_gbp[['Year', 'USD_to_GBP']]

# ==========================================
# 3. CALCULATE CNY TO LOCAL CURRENCY RATES
# ==========================================

# Merge all exchange rates by Year
df_rates = df_cny_usd.copy()
df_rates = df_rates.merge(df_usd_jpy, on='Year', how='outer')
df_rates = df_rates.merge(df_usd_krw, on='Year', how='outer')
df_rates = df_rates.merge(df_usd_myr, on='Year', how='outer')
df_rates = df_rates.merge(df_usd_sgd, on='Year', how='outer')
df_rates = df_rates.merge(df_usd_aud, on='Year', how='outer')
df_rates = df_rates.merge(df_usd_gbp, on='Year', how='outer')

# Calculate CNY per Destination Currency using the correct formulas:
# 
# FILE NAME CONVENTION:
# - "chinese_yuan_to_usa" = CNY per USD (e.g., 7.1 CNY = 1 USD)
# - "Japan_USA" or "Korean_won_to_usa" = Foreign Currency per USD (e.g., 110 JPY = 1 USD)
# - "USA_To_Australia" or "USA_to_UK" = USD per Foreign Currency (e.g., 1.5 USD = 1 GBP)
#
# FORMULAS:
# 1. For "Foreign per USD" (Standard Quotes): CNY_per_Destination = CNY_per_USD / Foreign_per_USD
#    Example: 7.1 CNY/USD ÷ 35 THB/USD = 0.202 CNY/THB
#
# 2. For "USD per Foreign" (Inverted Quotes): CNY_per_Destination = CNY_per_USD × USD_per_Foreign
#    Example: 7.1 CNY/USD × 1.25 USD/GBP = 8.875 CNY/GBP

# Standard Quotes (Foreign per USD) - use DIVISION
df_rates['CNY_per_JPY'] = df_rates['CNY_to_USD'] / df_rates['USD_to_JPY']
df_rates['CNY_per_KRW'] = df_rates['CNY_to_USD'] / df_rates['USD_to_KRW']
df_rates['CNY_per_MYR'] = df_rates['CNY_to_USD'] / df_rates['USD_to_MYR']
df_rates['CNY_per_SGD'] = df_rates['CNY_to_USD'] / df_rates['USD_to_SGD']

# Inverted Quotes (USD per Foreign) - use MULTIPLICATION
df_rates['CNY_per_AUD'] = df_rates['CNY_to_USD'] * df_rates['USD_to_AUD']
df_rates['CNY_per_GBP'] = df_rates['CNY_to_USD'] * df_rates['USD_to_GBP']

# For USA, it's just the CNY to USD rate
df_rates['CNY_per_USD'] = df_rates['CNY_to_USD']

# ==========================================
# 4. MAP COUNTRIES TO EXCHANGE RATES
# ==========================================

def get_exchange_rate(row):
    """Get the appropriate CNY per Destination Currency exchange rate for each country"""
    year = row['Year']
    country = row['Country']
    
    # Get the rates for this year
    rates_year = df_rates[df_rates['Year'] == year]
    
    if rates_year.empty:
        return np.nan
    
    rates_year = rates_year.iloc[0]
    
    # Map country to appropriate exchange rate (CNY per Destination Currency)
    # Higher number = Destination currency is MORE EXPENSIVE for Chinese tourists
    if country == 'United States of America':
        return rates_year['CNY_per_USD']
    elif country == 'Japan':
        return rates_year['CNY_per_JPY']
    elif country == 'Korea, Republic of':
        return rates_year['CNY_per_KRW']
    elif country == 'Malaysia':
        return rates_year['CNY_per_MYR']
    elif country == 'Singapore':
        return rates_year['CNY_per_SGD']
    elif country == 'Australia':
        return rates_year['CNY_per_AUD']
    elif country == 'United Kingdom':
        return rates_year['CNY_per_GBP']
    else:
        # For countries without exchange rate data, use CNY per USD as proxy
        return rates_year['CNY_per_USD']

# Apply the function to get exchange rates
df_primary['exchange_rate'] = df_primary.apply(get_exchange_rate, axis=1)

# ==========================================
# 5. SAVE UPDATED DATASET
# ==========================================
output_filename = 'Primary_Dataset_For_Panel_FINAL.csv'
df_primary.to_csv(output_filename, index=False)

print(f"✓ Exchange rates added successfully!")
print(f"✓ All rates are now: CNY per Destination Currency")
print(f"✓ Higher value = Destination is MORE EXPENSIVE for Chinese tourists")
print(f"✓ Saved to: {output_filename}")
print(f"\nSample data for different countries (2020):")
sample = df_primary[df_primary['Year'] == 2020][['Country', 'Year', 'exchange_rate']].head(10)
print(sample.to_string(index=False))

print(f"\nExample interpretation (2020):")
print(f"- If CNY_per_JPY = 0.064, then 1 Japanese Yen costs 0.064 Chinese Yuan")
print(f"- If CNY_per_USD = 6.90, then 1 US Dollar costs 6.90 Chinese Yuan")

print(f"\nExchange rate coverage:")
print(f"Total rows: {len(df_primary)}")
print(f"Rows with exchange rate: {df_primary['exchange_rate'].notna().sum()}")
print(f"Rows missing exchange rate: {df_primary['exchange_rate'].isna().sum()}")
