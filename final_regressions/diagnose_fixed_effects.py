import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'cpi_index', 'exchange_rate'])

print("=" * 70)
print("DIAGNOSING FIXED EFFECTS ISSUES")
print("=" * 70)

# Check time trends
print("\n1. TIME TRENDS (Do variables trend over time?)")
print("-" * 70)

yearly_avg = df.groupby('Year').agg({
    'cpi_index': 'mean',
    'exchange_rate': 'mean',
    'peace_index': 'mean',
    'arrivals_from_china': 'mean'
}).reset_index()

# Calculate correlation with time
from scipy.stats import pearsonr

for var in ['cpi_index', 'exchange_rate', 'peace_index', 'arrivals_from_china']:
    corr, pval = pearsonr(yearly_avg['Year'], yearly_avg[var])
    print(f"{var:25s}: correlation with Year = {corr:6.3f} (p={pval:.4f})")
    if abs(corr) > 0.7:
        print(f"  ❌ STRONG time trend - will conflict with time fixed effects!")
    elif abs(corr) > 0.4:
        print(f"  ⚠️  MODERATE time trend")
    else:
        print(f"  ✓ Weak time trend")

print("\n2. WITHIN-COUNTRY VARIATION (Do variables vary within countries?)")
print("-" * 70)

# Calculate within-country variation
for var in ['cpi_index', 'exchange_rate', 'peace_index', 'arrivals_from_china']:
    # Total variance
    total_var = df[var].var()
    
    # Between-country variance (variance of country means)
    country_means = df.groupby('Country')[var].mean()
    between_var = country_means.var()
    
    # Within-country variance
    within_var = total_var - between_var
    
    # Percentage within
    pct_within = (within_var / total_var) * 100
    
    print(f"{var:25s}: {pct_within:5.1f}% of variation is within-country")
    if pct_within < 10:
        print(f"  ❌ Very little within-country variation - entity FE will absorb most signal!")
    elif pct_within < 30:
        print(f"  ⚠️  Low within-country variation")
    else:
        print(f"  ✓ Good within-country variation")

print("\n3. RECOMMENDATION")
print("=" * 70)
print("""
The high VIF is likely due to TIME FIXED EFFECTS absorbing variation in CPI and Peace Index.

SOLUTIONS:

Option 1: Remove Time Fixed Effects
   - Keep entity_effects=True, set time_effects=False
   - Pro: Allows CPI and Peace Index to vary over time
   - Con: Doesn't control for global shocks (COVID, etc.)

Option 2: Use First Differences
   - Instead of levels, use year-over-year changes
   - Pro: Removes time trends automatically
   - Con: Loses long-run relationships

Option 3: Detrend Variables
   - Remove linear time trends from CPI and Peace Index
   - Pro: Keeps both fixed effects
   - Con: More complex interpretation

Option 4: Drop CPI or Peace Index
   - Keep only the most important variable
   - Pro: Simple, clean model
   - Con: Omitted variable bias

RECOMMENDED: Try Option 1 first (remove time fixed effects)
""")
