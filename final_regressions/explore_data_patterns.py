import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'cpi_index', 'exchange_rate'])

print("=" * 70)
print("DATA EXPLORATION: Understanding the Patterns")
print("=" * 70)

# 1. Check Thailand specifically
print("\n1. THAILAND PATTERN (2020-2024)")
print("-" * 70)
thailand = df[df['Country'] == 'Thailand'].sort_values('Year')
thailand_recent = thailand[thailand['Year'] >= 2020][['Year', 'arrivals_from_china', 'cpi_index', 'exchange_rate', 'peace_index']]
print(thailand_recent.to_string(index=False))

print("\n2. THAILAND PENALTY CHECK")
print("-" * 70)
thailand_pre = thailand[thailand['Year'] < 2023]['arrivals_from_china'].mean()
thailand_post = thailand[thailand['Year'] >= 2023]['arrivals_from_china'].mean()
print(f"Average arrivals BEFORE 2023: {thailand_pre:,.0f}")
print(f"Average arrivals AFTER 2023:  {thailand_post:,.0f}")
print(f"Change: {((thailand_post/thailand_pre - 1) * 100):+.1f}%")

if thailand_post > thailand_pre:
    print("❌ Thailand actually had MORE tourists after 2023, not fewer!")
    print("   The 'penalty' variable is capturing a BOOST, not a drop")

# 3. Check all countries 2023-2024
print("\n3. ALL COUNTRIES: 2023-2024 PATTERN")
print("-" * 70)
recent = df[df['Year'].isin([2023, 2024])].groupby('Country')['arrivals_from_china'].mean().sort_values(ascending=False)
print(recent.to_string())

# 4. Check if there's actually variation in the data
print("\n4. VARIATION CHECK")
print("-" * 70)
print(f"Arrivals range: {df['arrivals_from_china'].min():,.0f} to {df['arrivals_from_china'].max():,.0f}")
print(f"CPI range: {df['cpi_index'].min():.1f} to {df['cpi_index'].max():.1f}")
print(f"Exchange rate range: {df['exchange_rate'].min():.4f} to {df['exchange_rate'].max():.4f}")
print(f"Peace index range: {df['peace_index'].min():.3f} to {df['peace_index'].max():.3f}")

# 5. Check COVID impact
print("\n5. COVID IMPACT (2020 vs 2019)")
print("-" * 70)
covid_impact = df[df['Year'].isin([2019, 2020])].groupby(['Country', 'Year'])['arrivals_from_china'].mean().unstack()
if 2019 in covid_impact.columns and 2020 in covid_impact.columns:
    covid_impact['Change %'] = ((covid_impact[2020] / covid_impact[2019] - 1) * 100)
    print(covid_impact.sort_values('Change %').to_string())

# 6. Simple correlations
print("\n6. SIMPLE CORRELATIONS (Without Fixed Effects)")
print("-" * 70)
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['cpi_index'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

correlations = df[['ln_arrivals', 'ln_cpi', 'ln_exchange_rate', 'peace_index']].corr()['ln_arrivals'].drop('ln_arrivals')
print(correlations.to_string())

print("\n7. RECOMMENDATION")
print("=" * 70)
print("""
Based on the patterns above, consider:

1. If Thailand had MORE tourists after 2023, rename 'thailand_penalty' to 'thailand_boost'
   or flip the interaction term

2. COVID (2020-2021) is likely dominating all other effects
   - Consider adding a COVID dummy variable
   - Or exclude 2020-2021 from the analysis

3. The model might need:
   - Lagged variables (effects take time)
   - GDP controls (Chinese economic growth)
   - Visa policy changes
   
4. Consider a simpler model first:
   - Just entity fixed effects + year dummies
   - Add variables one at a time to see which matter
""")
