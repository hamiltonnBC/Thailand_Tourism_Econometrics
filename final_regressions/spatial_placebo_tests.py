"""
Spatial Placebo Tests for Thailand Asymmetry Analysis

This script runs Model C (Thailand Asymmetry) for each country in the sample,
replacing Thailand with each other country as a placebo test.

If Thailand's effect is unique, only Thailand should show a significant coefficient.
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. LOAD DATA
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'Primary_Dataset_For_Panel_FINAL.csv')
df = pd.read_csv(data_path)

# Filter data (same as Model C)
countries_to_include = ['Australia', 'Cambodia', 'Indonesia', 'Japan', 
                        'Malaysia', 'Maldives', 'Singapore', 'Thailand', 'Viet Nam']

df = df[(df['Country'].isin(countries_to_include)) & 
        (df['Year'] >= 2008) & 
        (df['Year'] <= 2024)]

df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'CPI_destination', 
                       'gdp_china', 'exchange_rate'])

print("=" * 80)
print("SPATIAL PLACEBO TESTS - ALL COUNTRIES")
print("=" * 80)
print(f"Testing {len(countries_to_include)} countries")
print(f"Total observations: {len(df)}")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
print()

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['CPI_destination'])
df['ln_gdp_china'] = np.log(df['gdp_china'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

# COVID variables
df['covid_dummy'] = ((df['Year'] >= 2020) & (df['Year'] <= 2021)).astype(int)
df['post_covid'] = (df['Year'] >= 2022).astype(int)

# Set panel structure
df = df.set_index(['Country', 'Year'])

# ==========================================
# 3. RUN PLACEBO TESTS FOR ALL COUNTRIES
# ==========================================
placebo_results = []

for country in countries_to_include:
    print(f"\n{'='*80}")
    print(f"PLACEBO TEST: {country}")
    print(f"{'='*80}")
    
    # Create interaction term for this country
    df_test = df.copy()
    df_test = df_test.reset_index()
    df_test[f'is_{country}'] = (df_test['Country'] == country).astype(int)
    df_test[f'{country}_post_covid'] = df_test[f'is_{country}'] * df_test['post_covid']
    df_test = df_test.set_index(['Country', 'Year'])
    
    # Run Model C with this country's interaction
    exog_vars = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 
                 'covid_dummy', 'post_covid', f'{country}_post_covid']
    
    exog = sm.add_constant(df_test[exog_vars])
    
    try:
        mod = PanelOLS(df_test['ln_arrivals'], exog, entity_effects=True, time_effects=False)
        res = mod.fit(cov_type='clustered', cluster_entity=True)
        
        # Extract results for the interaction term
        interaction_coef = res.params[f'{country}_post_covid']
        interaction_se = res.std_errors[f'{country}_post_covid']
        interaction_tstat = res.tstats[f'{country}_post_covid']
        interaction_pval = res.pvalues[f'{country}_post_covid']
        
        # Determine if significant
        is_significant = interaction_pval < 0.05
        
        placebo_results.append({
            'country': country,
            'coefficient': interaction_coef,
            'std_error': interaction_se,
            't_stat': interaction_tstat,
            'p_value': interaction_pval,
            'significant': is_significant,
            'is_thailand': country == 'Thailand'
        })
        
        print(f"\nCoefficient: {interaction_coef:.4f}")
        print(f"Std Error:   {interaction_se:.4f}")
        print(f"t-statistic: {interaction_tstat:.4f}")
        print(f"p-value:     {interaction_pval:.4f}")
        print(f"Significant: {'YES' if is_significant else 'NO'}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        placebo_results.append({
            'country': country,
            'coefficient': np.nan,
            'std_error': np.nan,
            't_stat': np.nan,
            'p_value': np.nan,
            'significant': False,
            'is_thailand': country == 'Thailand'
        })

# ==========================================
# 4. SUMMARY TABLE
# ==========================================
print("\n" + "=" * 80)
print("SUMMARY OF PLACEBO TESTS")
print("=" * 80)

results_df = pd.DataFrame(placebo_results)
results_df = results_df.sort_values('p_value')

print("\nRanked by p-value (most significant first):")
print(results_df[['country', 'coefficient', 't_stat', 'p_value', 'significant']].to_string(index=False))

# Count significant results
n_significant = results_df['significant'].sum()
print(f"\n{n_significant} out of {len(countries_to_include)} countries show significant effects (p < 0.05)")

# Check if only Thailand is significant
thailand_only = (results_df[results_df['is_thailand']]['significant'].iloc[0] and 
                 results_df[~results_df['is_thailand']]['significant'].sum() == 0)

print("\n" + "=" * 80)
print("INTERPRETATION")
print("=" * 80)

if thailand_only:
    print("✓ SUCCESS: Only Thailand shows a significant effect!")
    print("  This strongly supports the claim that Thailand's asymmetric recovery is unique.")
    print("  All other countries show no significant post-COVID interaction effect.")
elif n_significant == 0:
    print("✗ PROBLEM: No countries (including Thailand) show significant effects!")
    print("  This suggests the model specification may need adjustment.")
elif n_significant > 1:
    print(f"⚠ CAUTION: {n_significant} countries show significant effects.")
    print("  This suggests the asymmetric recovery may not be Thailand-specific.")
    print("  Significant countries:")
    for _, row in results_df[results_df['significant']].iterrows():
        print(f"    - {row['country']}: β = {row['coefficient']:.4f}, p = {row['p_value']:.4f}")

# ==========================================
# 5. VISUALIZATION
# ==========================================
print("\n" + "=" * 80)
print("GENERATING VISUALIZATION")
print("=" * 80)

# Create coefficient plot with confidence intervals
fig, ax = plt.subplots(figsize=(12, 8))

# Sort by coefficient value
results_df = results_df.sort_values('coefficient', ascending=True)

# Calculate 95% confidence intervals
results_df['ci_lower'] = results_df['coefficient'] - 1.96 * results_df['std_error']
results_df['ci_upper'] = results_df['coefficient'] + 1.96 * results_df['std_error']

# Color code: Thailand = blue, significant others = red, non-significant = green
colors = []
for _, row in results_df.iterrows():
    if row['is_thailand']:
        colors.append('#3b82f6' if row['significant'] else '#fca5a5')
    elif row['significant']:
        colors.append('#ef4444')
    else:
        colors.append('#22c55e')

# Plot
y_pos = np.arange(len(results_df))
ax.barh(y_pos, results_df['coefficient'], color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# Add confidence intervals
for i, (_, row) in enumerate(results_df.iterrows()):
    ax.plot([row['ci_lower'], row['ci_upper']], [i, i], 'k-', linewidth=2)
    ax.plot([row['ci_lower'], row['ci_lower']], [i-0.2, i+0.2], 'k-', linewidth=2)
    ax.plot([row['ci_upper'], row['ci_upper']], [i-0.2, i+0.2], 'k-', linewidth=2)

# Add zero line
ax.axvline(x=0, color='black', linestyle='--', linewidth=2, alpha=0.5)

# Labels
ax.set_yticks(y_pos)
ax.set_yticklabels(results_df['country'])
ax.set_xlabel('Coefficient (Country × Post-COVID)', fontsize=12, fontweight='bold')
ax.set_title('Spatial Placebo Tests: Post-COVID Recovery by Country\n(95% Confidence Intervals)', 
             fontsize=14, fontweight='bold')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#3b82f6', edgecolor='black', label='Thailand (Significant)'),
    Patch(facecolor='#22c55e', edgecolor='black', label='Other Countries (Not Significant)'),
    Patch(facecolor='#ef4444', edgecolor='black', label='Other Countries (Significant - Problem!)')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

# Grid
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'spatial_placebo_tests.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: spatial_placebo_tests.png")

# ==========================================
# 6. SAVE RESULTS
# ==========================================
results_df.to_csv(os.path.join(script_dir, 'spatial_placebo_results.csv'), index=False)
print("✓ Saved: spatial_placebo_results.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
