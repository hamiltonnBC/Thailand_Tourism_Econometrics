import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm

# ==========================================
# 1. LOAD YOUR DATA
# ==========================================
df = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')

# Drop rows with missing values in key variables
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'cpi_index', 'exchange_rate'])

print(f"Initial: {len(df)} observations across {df['Country'].nunique()} countries")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")

# ==========================================
# 2. HANDLE COVID PERIOD
# ==========================================
# Option A: Exclude COVID years (2020-2021) - RECOMMENDED
print("\n⚠️  Excluding 2020-2021 (COVID period) for cleaner analysis")
df = df[~df['Year'].isin([2020, 2021])]

# Option B: Add COVID dummy (uncomment if you want to keep 2020-2021)
# df['covid_period'] = df['Year'].isin([2020, 2021]).astype(int)

print(f"After COVID exclusion: {len(df)} observations")

# ==========================================
# 3. FEATURE ENGINEERING
# ==========================================

# A. Log Transformations
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['cpi_index'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

# B. Create interaction terms
# Thailand effect (2023+) - renamed to "boost" since it's positive
df['is_thailand'] = (df['Country'] == 'Thailand').astype(int)
df['post_2023'] = (df['Year'] >= 2023).astype(int)
df['thailand_post2023'] = df['is_thailand'] * df['post_2023']

# C. Add year dummies to capture time trends
df['year_2023'] = (df['Year'] == 2023).astype(int)
df['year_2024'] = (df['Year'] == 2024).astype(int)

# ==========================================
# 4. SET UP PANEL DATA STRUCTURE
# ==========================================
df = df.set_index(['Country', 'Year'])

# ==========================================
# 5. MODEL 1: BASELINE (No Thailand interaction)
# ==========================================
print("\n" + "=" * 70)
print("MODEL 1: BASELINE (Economic factors only)")
print("=" * 70)

exog_vars_1 = ['ln_cpi', 'ln_exchange_rate', 'peace_index']
exog_1 = sm.add_constant(df[exog_vars_1])

mod_1 = PanelOLS(df['ln_arrivals'], exog_1, entity_effects=True, time_effects=False)
res_1 = mod_1.fit(cov_type='clustered', cluster_entity=True)

print(res_1)

# ==========================================
# 6. MODEL 2: WITH THAILAND INTERACTION
# ==========================================
print("\n" + "=" * 70)
print("MODEL 2: WITH THAILAND POST-2023 EFFECT")
print("=" * 70)

exog_vars_2 = ['ln_cpi', 'ln_exchange_rate', 'peace_index', 'thailand_post2023']
exog_2 = sm.add_constant(df[exog_vars_2])

mod_2 = PanelOLS(df['ln_arrivals'], exog_2, entity_effects=True, time_effects=False)
res_2 = mod_2.fit(cov_type='clustered', cluster_entity=True)

print(res_2)

# ==========================================
# 7. MODEL 3: WITH YEAR DUMMIES
# ==========================================
print("\n" + "=" * 70)
print("MODEL 3: WITH YEAR DUMMIES (2023, 2024)")
print("=" * 70)

exog_vars_3 = ['ln_cpi', 'ln_exchange_rate', 'peace_index', 'thailand_post2023', 'year_2023', 'year_2024']
exog_3 = sm.add_constant(df[exog_vars_3])

mod_3 = PanelOLS(df['ln_arrivals'], exog_3, entity_effects=True, time_effects=False)
res_3 = mod_3.fit(cov_type='clustered', cluster_entity=True)

print(res_3)

# ==========================================
# 8. INTERPRETATION
# ==========================================
print("\n" + "=" * 70)
print("INTERPRETATION GUIDE")
print("=" * 70)

print("\nMODEL 2 COEFFICIENTS:")
params = res_2.params
pvals = res_2.pvalues

for var in exog_vars_2:
    coef = params[var]
    pval = pvals[var]
    sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
    
    if var == 'ln_cpi':
        print(f"\n{var}: {coef:.4f} {sig}")
        print(f"  → 1% increase in CPI → {coef:.2f}% change in arrivals")
        print(f"  → p-value: {pval:.4f}")
    elif var == 'ln_exchange_rate':
        print(f"\n{var}: {coef:.4f} {sig}")
        print(f"  → 1% more expensive destination → {coef:.2f}% change in arrivals")
        print(f"  → p-value: {pval:.4f}")
    elif var == 'peace_index':
        print(f"\n{var}: {coef:.4f} {sig}")
        print(f"  → 1 point more dangerous → {coef*100:.2f}% change in arrivals")
        print(f"  → p-value: {pval:.4f}")
    elif var == 'thailand_post2023':
        print(f"\n{var}: {coef:.4f} {sig}")
        print(f"  → Thailand in 2023+ has {coef*100:.2f}% different arrivals vs trend")
        print(f"  → p-value: {pval:.4f}")

print("\n" + "=" * 70)
print("NOTES:")
print("- *** p<0.01, ** p<0.05, * p<0.1")
print("- Negative coefficient = inverse relationship")
print("- Positive coefficient = direct relationship")
print("=" * 70)
