"""
=================================================================================
SPATIAL PLACEBO TESTS FOR THAILAND ASYMMETRY ANALYSIS
=================================================================================

This script performs comprehensive spatial placebo tests to validate whether
Thailand's asymmetric post-COVID recovery is truly Thailand-specific or if it's
a broader regional/random phenomenon.

METHODOLOGY:
- Run Model C (Thailand Asymmetry) for each country in the sample
- Replace Thailand with each other country as a placebo treatment
- Compare coefficients and significance levels

EXPECTED RESULT:
- Only Thailand should show a significant post-COVID interaction effect
- All other countries should have p-values > 0.10 (not significant)

If multiple countries show significant effects, it suggests the pattern is
regional or systematic, not Thailand-specific.

Author: Nicholas Hamilton
Date: December 2024
=================================================================================
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

print("=" * 85)
print("SPATIAL PLACEBO TESTS - THAILAND ASYMMETRY VALIDATION")
print("=" * 85)
print(f"Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ==========================================
# 1. LOAD AND PREPARE DATA
# ==========================================
print("STEP 1: Loading and preparing data...")
print("-" * 85)

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'Primary_Dataset_For_Panel_FINAL.csv')

try:
    df = pd.read_csv(data_path)
    print(f"✓ Successfully loaded data from: {data_path}")
except FileNotFoundError:
    print(f"✗ ERROR: Could not find data file at {data_path}")
    exit(1)

# Filter data (same specification as Model C)
countries_to_include = ['Australia', 'Cambodia', 'Indonesia', 'Japan', 
                        'Malaysia', 'Maldives', 'Singapore', 'Thailand', 'Viet Nam']

df = df[(df['Country'].isin(countries_to_include)) & 
        (df['Year'] >= 2008) & 
        (df['Year'] <= 2024)]

print(f"✓ Filtered to {len(countries_to_include)} countries: {', '.join(countries_to_include)}")
print(f"✓ Year range: {df['Year'].min()} - {df['Year'].max()}")
print(f"✓ Total observations before cleaning: {len(df)}")

# Drop missing values
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'CPI_destination', 
                       'gdp_china', 'exchange_rate'])

print(f"✓ Total observations after cleaning: {len(df)}")
print(f"✓ Observations per country:")
for country in countries_to_include:
    n_obs = len(df[df['Country'] == country])
    print(f"    {country:15s}: {n_obs:3d} observations")

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
print("\n" + "=" * 85)
print("STEP 2: Feature engineering...")
print("-" * 85)

# Log transformations
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['CPI_destination'])
df['ln_gdp_china'] = np.log(df['gdp_china'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

print("✓ Applied log transformations to: arrivals, CPI, GDP, exchange rate")

# COVID period variables
df['covid_dummy'] = ((df['Year'] >= 2020) & (df['Year'] <= 2021)).astype(int)
df['post_covid'] = (df['Year'] >= 2022).astype(int)

n_covid = df['covid_dummy'].sum()
n_post_covid = df['post_covid'].sum()
print(f"✓ Created COVID dummy: {n_covid} observations in COVID period (2020-2021)")
print(f"✓ Created post-COVID dummy: {n_post_covid} observations in post-COVID period (2022+)")

# Set panel structure
df = df.set_index(['Country', 'Year'])
print("✓ Set panel structure with Country and Year as indices")

# ==========================================
# 3. RUN PLACEBO TESTS FOR ALL COUNTRIES
# ==========================================
print("\n" + "=" * 85)
print("STEP 3: Running placebo regressions for all countries...")
print("=" * 85)
print("\nThis will take a moment. Running 8 separate panel regressions...\n")

placebo_results = []
detailed_results = {}

for i, country in enumerate(countries_to_include, 1):
    print(f"\n[{i}/{len(countries_to_include)}] Testing: {country}")
    print("-" * 85)
    
    # Create interaction term for this country
    df_test = df.copy()
    df_test = df_test.reset_index()
    df_test[f'is_{country}'] = (df_test['Country'] == country).astype(int)
    df_test[f'{country}_post_covid'] = df_test[f'is_{country}'] * df_test['post_covid']
    df_test = df_test.set_index(['Country', 'Year'])
    
    # Model C specification with this country's interaction
    exog_vars = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 
                 'covid_dummy', 'post_covid', f'{country}_post_covid']
    
    exog = sm.add_constant(df_test[exog_vars])
    
    try:
        # Estimate model
        mod = PanelOLS(df_test['ln_arrivals'], exog, entity_effects=True, time_effects=False)
        res = mod.fit(cov_type='clustered', cluster_entity=True)
        
        # Extract results for the interaction term
        interaction_coef = res.params[f'{country}_post_covid']
        interaction_se = res.std_errors[f'{country}_post_covid']
        interaction_tstat = res.tstats[f'{country}_post_covid']
        interaction_pval = res.pvalues[f'{country}_post_covid']
        
        # Calculate confidence intervals
        ci_lower = interaction_coef - 1.96 * interaction_se
        ci_upper = interaction_coef + 1.96 * interaction_se
        
        # Determine if significant at different levels
        sig_01 = interaction_pval < 0.01
        sig_05 = interaction_pval < 0.05
        sig_10 = interaction_pval < 0.10
        
        # Store results
        placebo_results.append({
            'country': country,
            'coefficient': interaction_coef,
            'std_error': interaction_se,
            't_stat': interaction_tstat,
            'p_value': interaction_pval,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'sig_01': sig_01,
            'sig_05': sig_05,
            'sig_10': sig_10,
            'is_thailand': country == 'Thailand',
            'r_squared': res.rsquared,
            'r_squared_within': res.rsquared_within,
            'n_obs': res.nobs
        })
        
        # Store full regression results
        detailed_results[country] = res
        
        # Print results
        print(f"  Coefficient:     {interaction_coef:8.4f}")
        print(f"  Std Error:       {interaction_se:8.4f}")
        print(f"  t-statistic:     {interaction_tstat:8.4f}")
        print(f"  p-value:         {interaction_pval:8.4f}")
        print(f"  95% CI:          [{ci_lower:7.4f}, {ci_upper:7.4f}]")
        print(f"  R² (within):     {res.rsquared_within:8.4f}")
        
        # Significance stars
        stars = ""
        if sig_01:
            stars = "***"
        elif sig_05:
            stars = "**"
        elif sig_10:
            stars = "*"
        
        if stars:
            print(f"  Significance:    {stars} (p < {0.01 if sig_01 else 0.05 if sig_05 else 0.10})")
        else:
            print(f"  Significance:    Not significant")
        
        # Special message for Thailand
        if country == 'Thailand':
            print(f"\n  → This is the BASELINE result (actual Thailand effect)")
            if sig_05:
                print(f"  → Thailand shows a significant effect (as expected from Model C)")
            else:
                print(f"  → WARNING: Thailand is not significant in this specification!")
        else:
            if sig_05:
                print(f"  → ⚠️  WARNING: {country} shows a significant effect!")
                print(f"  → This suggests the pattern may not be Thailand-specific")
            else:
                print(f"  → ✓ Good: {country} shows no significant effect (as expected)")
        
        print(f"  Status: ✓ SUCCESS")
        
    except Exception as e:
        print(f"  Status: ✗ ERROR - {str(e)}")
        placebo_results.append({
            'country': country,
            'coefficient': np.nan,
            'std_error': np.nan,
            't_stat': np.nan,
            'p_value': np.nan,
            'ci_lower': np.nan,
            'ci_upper': np.nan,
            'sig_01': False,
            'sig_05': False,
            'sig_10': False,
            'is_thailand': country == 'Thailand',
            'r_squared': np.nan,
            'r_squared_within': np.nan,
            'n_obs': np.nan
        })

# ==========================================
# 4. SUMMARY ANALYSIS
# ==========================================
print("\n" + "=" * 85)
print("STEP 4: Summary analysis and interpretation")
print("=" * 85)

results_df = pd.DataFrame(placebo_results)

# Sort by p-value
results_df_sorted = results_df.sort_values('p_value')

print("\n RESULTS RANKED BY SIGNIFICANCE (most significant first):")
print("-" * 85)
print(f"{'Country':<15} {'Coefficient':>12} {'t-stat':>10} {'p-value':>10} {'Sig':>5} {'Status':>15}")
print("-" * 85)

for _, row in results_df_sorted.iterrows():
    stars = ""
    if row['sig_01']:
        stars = "***"
    elif row['sig_05']:
        stars = "**"
    elif row['sig_10']:
        stars = "*"
    
    status = "THAILAND" if row['is_thailand'] else ("PROBLEM!" if row['sig_05'] else "Good")
    
    print(f"{row['country']:<15} {row['coefficient']:>12.4f} {row['t_stat']:>10.3f} "
          f"{row['p_value']:>10.4f} {stars:>5} {status:>15}")

# Count significant results
n_sig_01 = results_df['sig_01'].sum()
n_sig_05 = results_df['sig_05'].sum()
n_sig_10 = results_df['sig_10'].sum()

print("\n" + "=" * 85)
print("📈 SIGNIFICANCE SUMMARY:")
print("-" * 85)
print(f"  Countries significant at p < 0.01: {n_sig_01} / {len(countries_to_include)}")
print(f"  Countries significant at p < 0.05: {n_sig_05} / {len(countries_to_include)}")
print(f"  Countries significant at p < 0.10: {n_sig_10} / {len(countries_to_include)}")

# Check if only Thailand is significant
thailand_sig = results_df[results_df['is_thailand']]['sig_05'].iloc[0]
others_sig = results_df[~results_df['is_thailand']]['sig_05'].sum()

print("\n" + "=" * 85)
print("🎯 INTERPRETATION:")
print("=" * 85)

if thailand_sig and others_sig == 0:
    print("\n✅ EXCELLENT RESULT!")
    print("   Only Thailand shows a significant post-COVID interaction effect.")
    print("   All other countries show no significant effect (p > 0.05).")
    print("\n   CONCLUSION: This strongly supports the claim that Thailand's asymmetric")
    print("   recovery is UNIQUE and not a regional or random phenomenon.")
    print("\n   This is the ideal outcome for your spatial placebo test!")
    
elif not thailand_sig and others_sig == 0:
    print("\n⚠️  UNEXPECTED RESULT")
    print("   No countries (including Thailand) show significant effects.")
    print("\n   POSSIBLE EXPLANATIONS:")
    print("   - Model specification may need adjustment")
    print("   - Sample size or time period issues")
    print("   - The effect may be weaker than initially estimated")
    
elif thailand_sig and others_sig > 0:
    print(f"\n⚠️  MIXED RESULT")
    print(f"   Thailand shows a significant effect, BUT {others_sig} other country(ies) also significant.")
    print("\n   Significant countries:")
    for _, row in results_df[(results_df['sig_05']) & (~results_df['is_thailand'])].iterrows():
        print(f"   - {row['country']}: β = {row['coefficient']:.4f}, p = {row['p_value']:.4f}")
    print("\n   INTERPRETATION:")
    print("   The asymmetric recovery pattern may not be Thailand-specific.")
    print("   Consider investigating what these countries have in common.")
    print("   Possible explanations:")
    print("   - Regional Southeast Asian effect")
    print("   - Similar tourism profiles or policies")
    print("   - Data quality issues in post-COVID period")
    
else:
    print("\n❌ PROBLEMATIC RESULT")
    print("   Thailand is NOT significant, but other countries are.")
    print("   This contradicts the Model C findings and requires investigation.")

# Additional statistics
print("\n" + "=" * 85)
print("📊 COEFFICIENT STATISTICS:")
print("-" * 85)
print(f"  Mean coefficient:     {results_df['coefficient'].mean():8.4f}")
print(f"  Median coefficient:   {results_df['coefficient'].median():8.4f}")
print(f"  Std deviation:        {results_df['coefficient'].std():8.4f}")
print(f"  Min coefficient:      {results_df['coefficient'].min():8.4f} ({results_df.loc[results_df['coefficient'].idxmin(), 'country']})")
print(f"  Max coefficient:      {results_df['coefficient'].max():8.4f} ({results_df.loc[results_df['coefficient'].idxmax(), 'country']})")

thailand_coef = results_df[results_df['is_thailand']]['coefficient'].iloc[0]
print(f"\n  Thailand coefficient: {thailand_coef:8.4f}")
print(f"  Thailand rank:        {(results_df['coefficient'] > thailand_coef).sum() + 1} / {len(countries_to_include)}")

# ==========================================
# 5. SAVE DETAILED RESULTS
# ==========================================
print("\n" + "=" * 85)
print("STEP 5: Saving results...")
print("=" * 85)

# Save summary table
output_csv = os.path.join(script_dir, 'spatial_placebo_results.csv')
results_df_sorted.to_csv(output_csv, index=False)
print(f"✓ Saved summary results: {output_csv}")

# Save detailed regression output
output_txt = os.path.join(script_dir, 'spatial_placebo_detailed_results.txt')
with open(output_txt, 'w') as f:
    f.write("=" * 85 + "\n")
    f.write("SPATIAL PLACEBO TESTS - DETAILED REGRESSION RESULTS\n")
    f.write("=" * 85 + "\n")
    f.write(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    for country in countries_to_include:
        if country in detailed_results:
            f.write("\n" + "=" * 85 + "\n")
            f.write(f"PLACEBO TEST: {country}\n")
            f.write("=" * 85 + "\n\n")
            f.write(str(detailed_results[country]))
            f.write("\n\n")

print(f"✓ Saved detailed regression output: {output_txt}")

# ==========================================
# 6. VISUALIZATIONS
# ==========================================
print("\n" + "=" * 85)
print("STEP 6: Creating visualizations...")
print("=" * 85)

# Visualization 1: Coefficient plot with confidence intervals
print("\n  Creating coefficient plot with confidence intervals...")

fig, ax = plt.subplots(figsize=(14, 8))

# Sort by coefficient value for better visualization
results_plot = results_df.sort_values('coefficient', ascending=True)

# Color code
colors = []
for _, row in results_plot.iterrows():
    if row['is_thailand']:
        colors.append('#3b82f6' if row['sig_05'] else '#93c5fd')  # Blue
    elif row['sig_05']:
        colors.append('#ef4444')  # Red - problematic
    else:
        colors.append('#22c55e')  # Green - good

# Plot bars
y_pos = np.arange(len(results_plot))
bars = ax.barh(y_pos, results_plot['coefficient'], color=colors, alpha=0.8, 
               edgecolor='black', linewidth=1.5)

# Add confidence intervals
for i, (_, row) in enumerate(results_plot.iterrows()):
    ax.plot([row['ci_lower'], row['ci_upper']], [i, i], 'k-', linewidth=2.5, alpha=0.8)
    ax.plot([row['ci_lower'], row['ci_lower']], [i-0.25, i+0.25], 'k-', linewidth=2.5)
    ax.plot([row['ci_upper'], row['ci_upper']], [i-0.25, i+0.25], 'k-', linewidth=2.5)
    
    # Add p-value labels
    x_pos = max(row['ci_upper'], row['coefficient']) + 0.05
    if row['sig_05']:
        ax.text(x_pos, i, f"p={row['p_value']:.3f}***" if row['sig_01'] else f"p={row['p_value']:.3f}**", 
                va='center', fontsize=9, fontweight='bold')

# Add zero line
ax.axvline(x=0, color='black', linestyle='--', linewidth=2, alpha=0.7, label='No Effect')

# Labels and formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(results_plot['country'], fontsize=11)
ax.set_xlabel('Coefficient (Country × Post-COVID Interaction)', fontsize=13, fontweight='bold')
ax.set_title('Spatial Placebo Tests: Post-COVID Recovery Effects by Country\n' + 
             '(95% Confidence Intervals | Entity Fixed Effects | Clustered SE)',
             fontsize=14, fontweight='bold', pad=20)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#3b82f6', edgecolor='black', label='Thailand (Significant - Expected)', alpha=0.8),
    Patch(facecolor='#22c55e', edgecolor='black', label='Other Countries (Not Significant - Good)', alpha=0.8),
    Patch(facecolor='#ef4444', edgecolor='black', label='Other Countries (Significant - Problem!)', alpha=0.8)
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.95)

# Grid
ax.grid(axis='x', alpha=0.3, linestyle=':', linewidth=1)
ax.set_axisbelow(True)

plt.tight_layout()
output_plot1 = os.path.join(script_dir, 'spatial_placebo_tests.png')
plt.savefig(output_plot1, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  ✓ Saved: spatial_placebo_tests.png")

# Visualization 2: P-value comparison
print("  Creating p-value comparison plot...")

fig, ax = plt.subplots(figsize=(12, 7))

# Sort by p-value
results_pval = results_df.sort_values('p_value', ascending=False)

# Color by significance
colors_pval = []
for _, row in results_pval.iterrows():
    if row['is_thailand']:
        colors_pval.append('#3b82f6')
    elif row['sig_05']:
        colors_pval.append('#ef4444')
    else:
        colors_pval.append('#22c55e')

y_pos = np.arange(len(results_pval))
ax.barh(y_pos, results_pval['p_value'], color=colors_pval, alpha=0.8, 
        edgecolor='black', linewidth=1.5)

# Add significance threshold lines
ax.axvline(x=0.01, color='red', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.01')
ax.axvline(x=0.05, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.05')
ax.axvline(x=0.10, color='yellow', linestyle='--', linewidth=2, alpha=0.7, label='p = 0.10')

# Labels
ax.set_yticks(y_pos)
ax.set_yticklabels(results_pval['country'], fontsize=11)
ax.set_xlabel('P-value', fontsize=13, fontweight='bold')
ax.set_title('Spatial Placebo Tests: Statistical Significance by Country\n' +
             '(Lower p-value = More significant effect)',
             fontsize=14, fontweight='bold', pad=20)

# Add value labels
for i, (_, row) in enumerate(results_pval.iterrows()):
    ax.text(row['p_value'] + 0.01, i, f"{row['p_value']:.4f}", 
            va='center', fontsize=9, fontweight='bold')

ax.legend(loc='lower right', fontsize=10, framealpha=0.95)
ax.grid(axis='x', alpha=0.3, linestyle=':', linewidth=1)
ax.set_axisbelow(True)
ax.set_xlim(0, max(results_pval['p_value'].max() * 1.1, 0.15))

plt.tight_layout()
output_plot2 = os.path.join(script_dir, 'spatial_placebo_pvalues.png')
plt.savefig(output_plot2, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  ✓ Saved: spatial_placebo_pvalues.png")

# Visualization 3: Coefficient distribution
print("  Creating coefficient distribution plot...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
ax1.hist(results_df[~results_df['is_thailand']]['coefficient'], bins=6, 
         color='#94a3b8', alpha=0.7, edgecolor='black', linewidth=1.5)
thailand_coef = results_df[results_df['is_thailand']]['coefficient'].iloc[0]
ax1.axvline(thailand_coef, color='#3b82f6', linestyle='--', linewidth=3, 
            label=f'Thailand (β = {thailand_coef:.4f})', alpha=0.9)
ax1.axvline(0, color='black', linestyle='-', linewidth=2, alpha=0.5, label='No Effect')
ax1.set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('Distribution of Placebo Coefficients\n(Excluding Thailand)', 
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3, linestyle=':', linewidth=1)

# Box plot
box_data = [results_df[~results_df['is_thailand']]['coefficient'].values]
bp = ax2.boxplot(box_data, vert=True, patch_artist=True, widths=0.5,
                 boxprops=dict(facecolor='#94a3b8', alpha=0.7, linewidth=2),
                 medianprops=dict(color='red', linewidth=2),
                 whiskerprops=dict(linewidth=2),
                 capprops=dict(linewidth=2))

# Add Thailand point
ax2.scatter([1], [thailand_coef], color='#3b82f6', s=200, zorder=5, 
            edgecolor='black', linewidth=2, label='Thailand', marker='D')
ax2.axhline(0, color='black', linestyle='-', linewidth=2, alpha=0.5)
ax2.set_ylabel('Coefficient Value', fontsize=12, fontweight='bold')
ax2.set_title('Coefficient Distribution: Thailand vs Others\n(Box Plot)', 
              fontsize=13, fontweight='bold')
ax2.set_xticklabels(['Other Countries'])
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3, linestyle=':', linewidth=1, axis='y')

plt.tight_layout()
output_plot3 = os.path.join(script_dir, 'spatial_placebo_distribution.png')
plt.savefig(output_plot3, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  ✓ Saved: spatial_placebo_distribution.png")

# ==========================================
# 7. FINAL SUMMARY
# ==========================================
print("\n" + "=" * 85)
print("✅ ANALYSIS COMPLETE!")
print("=" * 85)

print("\n📁 FILES GENERATED:")
print(f"  1. {output_csv}")
print(f"     → Summary table with coefficients, p-values, significance")
print(f"  2. {output_txt}")
print(f"     → Detailed regression output for all countries")
print(f"  3. {output_plot1}")
print(f"     → Coefficient plot with confidence intervals")
print(f"  4. {output_plot2}")
print(f"     → P-value comparison across countries")
print(f"  5. {output_plot3}")
print(f"     → Coefficient distribution analysis")

print("\n📊 QUICK SUMMARY:")
print(f"  • Total countries tested: {len(countries_to_include)}")
print(f"  • Significant at p < 0.05: {n_sig_05}")
print(f"  • Thailand coefficient: {thailand_coef:.4f}")
print(f"  • Thailand p-value: {results_df[results_df['is_thailand']]['p_value'].iloc[0]:.4f}")

print("\n🎯 NEXT STEPS:")
print("  1. Review the visualizations (PNG files)")
print("  2. Check the detailed results (TXT file)")
print("  3. Update the dashboard with actual values from CSV")
print("  4. Interpret findings in context of your research question")

print("\n" + "=" * 85)
print(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 85)
