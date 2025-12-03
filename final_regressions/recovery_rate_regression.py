import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# RECOVERY RATE REGRESSION ANALYSIS
# ==========================================
# This measures actual percentage recovery rates from 2019 baseline
# to test if Thailand is recovering slower than other countries

print("="*80)
print("RECOVERY RATE REGRESSION ANALYSIS")
print("="*80)

# Load data
df = pd.read_csv('Primary_Dataset_For_Panel_FINAL.csv')

# Filter for countries in the model (2008-2024)
countries = ['Australia', 'Cambodia', 'Indonesia', 'Japan', 
             'Malaysia', 'Singapore', 'Thailand', 'Viet Nam']
df = df[df['Country'].isin(countries)]

# ==========================================
# 1. CALCULATE RECOVERY RATE FOR EACH COUNTRY
# ==========================================

recovery_data = []

for country in countries:
    country_df = df[df['Country'] == country].sort_values('Year')
    
    # Get baseline (2019)
    baseline_2019 = country_df[country_df['Year'] == 2019]['arrivals_from_china'].values[0]
    
    # Get 2022 (start of recovery period)
    arrivals_2022 = country_df[country_df['Year'] == 2022]['arrivals_from_china'].values[0]
    
    # Get 2024 (end of recovery period)
    arrivals_2024 = country_df[country_df['Year'] == 2024]['arrivals_from_china'].values[0]
    
    # Calculate recovery rate (percentage points gained from 2022 to 2024)
    recovery_rate = ((arrivals_2024 - arrivals_2022) / baseline_2019) * 100
    
    # Get 2024 values for independent variables
    row_2024 = country_df[country_df['Year'] == 2024].iloc[0]
    
    recovery_data.append({
        'Country': country,
        'recovery_rate': recovery_rate,
        'baseline_2019': baseline_2019,
        'arrivals_2022': arrivals_2022,
        'arrivals_2024': arrivals_2024,
        'pct_2024_vs_2019': (arrivals_2024 / baseline_2019) * 100,
        'peace_index': row_2024['peace_index'],
        'cpi_index': row_2024['cpi_index'],
        'gdp_china': row_2024['gdp_china'],
        'exchange_rate': row_2024['exchange_rate'],
        'is_thailand': 1 if country == 'Thailand' else 0
    })

recovery_df = pd.DataFrame(recovery_data)

print("\n" + "-"*80)
print("RECOVERY RATE DATA (2022 → 2024)")
print("-"*80)
print(recovery_df[['Country', 'recovery_rate', 'pct_2024_vs_2019']].sort_values('recovery_rate', ascending=False))

# ==========================================
# 2. REGRESSION MODEL 1: Simple Thailand Dummy
# ==========================================

print("\n" + "="*80)
print("MODEL 1: Thailand Dummy Only")
print("="*80)

# Dependent variable
y = recovery_df['recovery_rate']

# Independent variable: Thailand dummy
X1 = recovery_df[['is_thailand']]
X1 = sm.add_constant(X1)

# Run regression
model1 = sm.OLS(y, X1).fit()
print(model1.summary())

print("\n--- INTERPRETATION ---")
print(f"Average recovery rate (non-Thailand): {model1.params['const']:.2f} percentage points")
print(f"Thailand's difference: {model1.params['is_thailand']:.2f} percentage points")
print(f"Thailand's total recovery rate: {model1.params['const'] + model1.params['is_thailand']:.2f} pp")

if model1.pvalues['is_thailand'] < 0.05:
    print(f"✓ Thailand's slower recovery is STATISTICALLY SIGNIFICANT (p = {model1.pvalues['is_thailand']:.3f})")
else:
    print(f"⚠️  Thailand's difference is NOT statistically significant (p = {model1.pvalues['is_thailand']:.3f})")

# ==========================================
# 3. REGRESSION MODEL 2: With Control Variables
# ==========================================

print("\n" + "="*80)
print("MODEL 2: Thailand Dummy + Control Variables")
print("="*80)

# Log transform continuous variables
recovery_df['ln_cpi'] = np.log(recovery_df['cpi_index'])
recovery_df['ln_gdp_china'] = np.log(recovery_df['gdp_china'])
recovery_df['ln_exchange_rate'] = np.log(recovery_df['exchange_rate'].abs())

# Independent variables
X2 = recovery_df[['is_thailand', 'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate']]
X2 = sm.add_constant(X2)

# Run regression
model2 = sm.OLS(y, X2).fit()
print(model2.summary())

print("\n--- INTERPRETATION ---")
print(f"Thailand effect (controlling for other factors): {model2.params['is_thailand']:.2f} pp")
print(f"Peace Index effect: {model2.params['peace_index']:.2f} pp per unit")
print(f"CPI effect: {model2.params['ln_cpi']:.2f} pp per 1% increase")

if model2.pvalues['is_thailand'] < 0.05:
    print(f"✓ Thailand effect is SIGNIFICANT (p = {model2.pvalues['is_thailand']:.3f})")
else:
    print(f"⚠️  Thailand effect is NOT significant (p = {model2.pvalues['is_thailand']:.3f})")

# ==========================================
# 4. REGRESSION MODEL 3: Baseline Size Control
# ==========================================

print("\n" + "="*80)
print("MODEL 3: Thailand Dummy + Baseline Size Control")
print("="*80)

# Add log of baseline size
recovery_df['ln_baseline'] = np.log(recovery_df['baseline_2019'])

# Independent variables
X3 = recovery_df[['is_thailand', 'ln_baseline', 'peace_index', 'ln_cpi']]
X3 = sm.add_constant(X3)

# Run regression
model3 = sm.OLS(y, X3).fit()
print(model3.summary())

print("\n--- INTERPRETATION ---")
print(f"Thailand effect (controlling for baseline size): {model3.params['is_thailand']:.2f} pp")
print(f"Baseline size effect: {model3.params['ln_baseline']:.2f} pp per 1% larger baseline")

# ==========================================
# 5. MODEL COMPARISON
# ==========================================

print("\n" + "="*80)
print("MODEL COMPARISON")
print("="*80)

comparison = pd.DataFrame({
    'Model 1 (Simple)': [model1.rsquared, model1.rsquared_adj, model1.fvalue, model1.nobs],
    'Model 2 (Full Controls)': [model2.rsquared, model2.rsquared_adj, model2.fvalue, model2.nobs],
    'Model 3 (Size Control)': [model3.rsquared, model3.rsquared_adj, model3.fvalue, model3.nobs]
}, index=['R-squared', 'Adj. R-squared', 'F-statistic', 'N'])
print(comparison)

# ==========================================
# 6. VISUALIZATIONS
# ==========================================

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# Plot 1: Recovery Rate by Country
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#FF6B6B' if c == 'Thailand' else '#4ECDC4' for c in recovery_df['Country']]
bars = ax.bar(recovery_df['Country'], recovery_df['recovery_rate'], color=colors, alpha=0.8, edgecolor='black')

# Add average line
avg_recovery = recovery_df['recovery_rate'].mean()
ax.axhline(y=avg_recovery, color='black', linestyle='--', linewidth=2, label=f'Average: {avg_recovery:.1f} pp')

ax.set_xlabel('Country', fontsize=12, fontweight='bold')
ax.set_ylabel('Recovery Rate (percentage points)', fontsize=12, fontweight='bold')
ax.set_title('Recovery Rate by Country (2022 → 2024)\nPercentage Points Gained Relative to 2019 Baseline', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('recovery_rate_by_country.png', dpi=300, bbox_inches='tight')
print("✓ Saved: recovery_rate_by_country.png")
plt.close()

# Plot 2: Actual vs Predicted (Model 2)
fig, ax = plt.subplots(figsize=(10, 8))
predicted = model2.fittedvalues
actual = y

for i, country in enumerate(recovery_df['Country']):
    color = '#FF6B6B' if country == 'Thailand' else '#4ECDC4'
    marker = 'o' if country == 'Thailand' else 's'
    size = 150 if country == 'Thailand' else 100
    ax.scatter(predicted.iloc[i], actual.iloc[i], s=size, color=color, 
               alpha=0.7, edgecolor='black', linewidth=2, marker=marker)
    ax.annotate(country, (predicted.iloc[i], actual.iloc[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)

# 45-degree line
min_val = min(predicted.min(), actual.min())
max_val = max(predicted.max(), actual.max())
ax.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, alpha=0.5, label='Perfect Fit')

ax.set_xlabel('Predicted Recovery Rate (pp)', fontsize=12, fontweight='bold')
ax.set_ylabel('Actual Recovery Rate (pp)', fontsize=12, fontweight='bold')
ax.set_title('Actual vs Predicted Recovery Rates\nModel 2 (with controls)', 
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('actual_vs_predicted_recovery.png', dpi=300, bbox_inches='tight')
print("✓ Saved: actual_vs_predicted_recovery.png")
plt.close()

# Plot 3: Residuals
fig, ax = plt.subplots(figsize=(10, 6))
residuals = model2.resid
colors = ['#FF6B6B' if c == 'Thailand' else '#4ECDC4' for c in recovery_df['Country']]

bars = ax.bar(recovery_df['Country'], residuals, color=colors, alpha=0.8, edgecolor='black')
ax.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax.set_xlabel('Country', fontsize=12, fontweight='bold')
ax.set_ylabel('Residual (pp)', fontsize=12, fontweight='bold')
ax.set_title('Model Residuals: Unexplained Recovery Rate\nNegative = Slower than expected', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('recovery_residuals.png', dpi=300, bbox_inches='tight')
print("✓ Saved: recovery_residuals.png")
plt.close()

# ==========================================
# 7. SAVE RESULTS
# ==========================================

# Save recovery data
recovery_df.to_csv('recovery_rate_data.csv', index=False)
print("✓ Saved: recovery_rate_data.csv")

# Save regression results
with open('recovery_rate_regression_results.txt', 'w') as f:
    f.write("="*80 + "\n")
    f.write("RECOVERY RATE REGRESSION RESULTS\n")
    f.write("="*80 + "\n\n")
    f.write("MODEL 1: Thailand Dummy Only\n")
    f.write("-"*80 + "\n")
    f.write(str(model1.summary()) + "\n\n")
    f.write("MODEL 2: Thailand Dummy + Controls\n")
    f.write("-"*80 + "\n")
    f.write(str(model2.summary()) + "\n\n")
    f.write("MODEL 3: Thailand Dummy + Baseline Size\n")
    f.write("-"*80 + "\n")
    f.write(str(model3.summary()) + "\n")

print("✓ Saved: recovery_rate_regression_results.txt")

# ==========================================
# 8. FINAL SUMMARY
# ==========================================

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

thailand_recovery = recovery_df[recovery_df['Country'] == 'Thailand']['recovery_rate'].values[0]
avg_recovery = recovery_df[recovery_df['Country'] != 'Thailand']['recovery_rate'].mean()

print(f"\nThailand's recovery rate: {thailand_recovery:.2f} percentage points")
print(f"Average of other countries: {avg_recovery:.2f} percentage points")
print(f"Difference: {thailand_recovery - avg_recovery:.2f} pp")

print(f"\nModel 1 Thailand coefficient: {model1.params['is_thailand']:.2f} (p = {model1.pvalues['is_thailand']:.3f})")
print(f"Model 2 Thailand coefficient: {model2.params['is_thailand']:.2f} (p = {model2.pvalues['is_thailand']:.3f})")
print(f"Model 3 Thailand coefficient: {model3.params['is_thailand']:.2f} (p = {model3.pvalues['is_thailand']:.3f})")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if model1.params['is_thailand'] < 0:
    print("\n✓ Thailand IS recovering SLOWER than other countries")
    print(f"  The recovery rate is {abs(model1.params['is_thailand']):.2f} pp lower than average")
    
    if model1.pvalues['is_thailand'] < 0.10:
        print(f"  This difference is statistically significant at 10% level")
    else:
        print(f"  However, this difference is NOT statistically significant")
        print(f"  (Small sample size: n={len(recovery_df)} countries)")
else:
    print("\n⚠️  Thailand is NOT recovering slower than other countries")

print("\n" + "="*80)
