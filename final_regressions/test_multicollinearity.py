import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD DATA
# ==========================================
df = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')

# Drop rows with missing values in key variables
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'cpi_index', 'exchange_rate'])

print(f"Loaded {len(df)} observations across {df['Country'].nunique()} countries")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}\n")

# ==========================================
# 2. CREATE LOG TRANSFORMATIONS
# ==========================================
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['cpi_index'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

# ==========================================
# 3. CORRELATION MATRIX
# ==========================================
print("=" * 70)
print("CORRELATION MATRIX")
print("=" * 70)

# Select the variables we're using in the regression
vars_to_test = ['ln_cpi', 'ln_exchange_rate', 'peace_index']
corr_matrix = df[vars_to_test].corr()

print("\nCorrelation Matrix:")
print(corr_matrix.round(3))

print("\n⚠️  INTERPRETATION:")
print("- Correlation > 0.8 or < -0.8: HIGH multicollinearity concern")
print("- Correlation 0.5 to 0.8: MODERATE concern")
print("- Correlation < 0.5: LOW concern")

# Highlight high correlations
print("\nHigh Correlations (|r| > 0.7):")
high_corr = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
            print(f"  - {corr_matrix.columns[i]} vs {corr_matrix.columns[j]}: {corr_matrix.iloc[i, j]:.3f}")

if not high_corr:
    print("  ✓ No high correlations detected!")

# ==========================================
# 4. VARIANCE INFLATION FACTOR (VIF)
# ==========================================
print("\n" + "=" * 70)
print("VARIANCE INFLATION FACTOR (VIF)")
print("=" * 70)

# Prepare data for VIF calculation
X = df[vars_to_test].copy()

# Calculate VIF for each variable
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print("\nVIF Values:")
print(vif_data.to_string(index=False))

print("\n⚠️  INTERPRETATION:")
print("- VIF = 1: No correlation with other variables")
print("- VIF 1-5: LOW multicollinearity (acceptable)")
print("- VIF 5-10: MODERATE multicollinearity (concerning)")
print("- VIF > 10: HIGH multicollinearity (problematic)")

print("\nVIF Assessment:")
for idx, row in vif_data.iterrows():
    var = row['Variable']
    vif = row['VIF']
    if vif > 10:
        print(f"  ❌ {var}: VIF = {vif:.2f} - HIGH multicollinearity!")
    elif vif > 5:
        print(f"  ⚠️  {var}: VIF = {vif:.2f} - MODERATE multicollinearity")
    else:
        print(f"  ✓ {var}: VIF = {vif:.2f} - Acceptable")

# ==========================================
# 5. SPECIFIC TEST: CPI vs EXCHANGE RATE
# ==========================================
print("\n" + "=" * 70)
print("SPECIFIC TEST: CPI INDEX vs EXCHANGE RATE")
print("=" * 70)

cpi_exch_corr = df[['ln_cpi', 'ln_exchange_rate']].corr().iloc[0, 1]
print(f"\nCorrelation between ln_cpi and ln_exchange_rate: {cpi_exch_corr:.4f}")

if abs(cpi_exch_corr) > 0.8:
    print("❌ SEVERE multicollinearity between CPI and Exchange Rate!")
    print("   Recommendation: Consider removing one variable or using interaction terms")
elif abs(cpi_exch_corr) > 0.5:
    print("⚠️  MODERATE correlation between CPI and Exchange Rate")
    print("   Recommendation: Proceed with caution, interpret coefficients carefully")
else:
    print("✓ LOW correlation - these variables can be used together safely")

# ==========================================
# 6. WITHIN-COUNTRY CORRELATION
# ==========================================
print("\n" + "=" * 70)
print("WITHIN-COUNTRY CORRELATION (Time-Series)")
print("=" * 70)
print("\nChecking if CPI and Exchange Rate move together WITHIN each country over time...")

within_corr = []
for country in df['Country'].unique():
    country_data = df[df['Country'] == country][['ln_cpi', 'ln_exchange_rate']].dropna()
    if len(country_data) > 2:  # Need at least 3 observations
        corr = country_data.corr().iloc[0, 1]
        within_corr.append({'Country': country, 'Correlation': corr})

within_corr_df = pd.DataFrame(within_corr).sort_values('Correlation', ascending=False)
print("\nWithin-Country Correlations:")
print(within_corr_df.to_string(index=False))

avg_within_corr = within_corr_df['Correlation'].mean()
print(f"\nAverage within-country correlation: {avg_within_corr:.4f}")

if abs(avg_within_corr) > 0.7:
    print("❌ HIGH within-country correlation - CPI and Exchange Rate move together over time")
    print("   This is problematic for fixed effects models!")
elif abs(avg_within_corr) > 0.4:
    print("⚠️  MODERATE within-country correlation")
else:
    print("✓ LOW within-country correlation - good for fixed effects!")

# ==========================================
# 7. RECOMMENDATIONS
# ==========================================
print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

if any(vif_data['VIF'] > 10):
    print("\n❌ HIGH MULTICOLLINEARITY DETECTED")
    print("   Options:")
    print("   1. Remove one of the highly correlated variables")
    print("   2. Combine them into a single index")
    print("   3. Use Ridge/Lasso regression instead of OLS")
elif any(vif_data['VIF'] > 5):
    print("\n⚠️  MODERATE MULTICOLLINEARITY DETECTED")
    print("   Options:")
    print("   1. Proceed but interpret coefficients carefully")
    print("   2. Check if standard errors are inflated")
    print("   3. Consider removing less important variables")
else:
    print("\n✓ NO SIGNIFICANT MULTICOLLINEARITY")
    print("   Your model should be fine!")

print("\n" + "=" * 70)
