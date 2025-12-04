"""
Heteroskedasticity and Autocorrelation Tests for Panel Data

This script runs:
1. Modified Wald Test for groupwise heteroskedasticity
2. Wooldridge Test for autocorrelation in panel data

Output:
- Test results (CSV and TXT)
- Visualization of residuals by country (PNG)
- Summary report
"""

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# ==========================================
# 1. LOAD AND PREPARE DATA
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'Primary_Dataset_For_Panel_FINAL.csv')
df = pd.read_csv(data_path)

# Filter data (same as main regression)
countries_to_include = ['Australia', 'Japan', 'Malaysia', 'Maldives', 
                        'Singapore', 'Thailand', 'Viet Nam', 'Cambodia', 'Indonesia']
df = df[(df['Country'].isin(countries_to_include)) & 
        (df['Year'] >= 2008) & 
        (df['Year'] <= 2024)]

df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'CPI_destination', 
                       'gdp_china', 'exchange_rate', 'RER'])

# Feature engineering
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['CPI_destination'])
df['ln_gdp_china'] = np.log(df['gdp_china'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])
df['RER_normalized'] = df.groupby('Country')['RER'].transform(lambda x: x / x.mean())
df['ln_rer'] = np.log(df['RER_normalized'])
df['covid_dummy'] = ((df['Year'] >= 2020) & (df['Year'] <= 2021)).astype(int)
df['post_covid'] = (df['Year'] >= 2022).astype(int)
df['is_thailand'] = (df['Country'] == 'Thailand').astype(int)
df['thailand_post_covid'] = df['is_thailand'] * df['post_covid']

print("=" * 80)
print("HETEROSKEDASTICITY AND AUTOCORRELATION TESTS")
print("=" * 80)
print(f"Sample: {len(df)} observations, {df['Country'].nunique()} countries")
print(f"Years: {df['Year'].min()}-{df['Year'].max()}")
print()

# ==========================================
# 2. DEFINE MODELS AND RUN REGRESSIONS
# ==========================================
models = {
    'Model A': {
        'vars': ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 'covid_dummy'],
        'name': 'Baseline (Nominal ER)'
    },
    'Model C': {
        'vars': ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 
                 'covid_dummy', 'post_covid', 'thailand_post_covid'],
        'name': 'Thailand Asymmetry (Nominal ER)'
    },
    'Model D': {
        'vars': ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 'covid_dummy'],
        'name': 'Baseline (RER)'
    },
    'Model F': {
        'vars': ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 
                 'covid_dummy', 'post_covid', 'thailand_post_covid'],
        'name': 'Thailand Asymmetry (RER)'
    }
}

# Set panel index
df = df.set_index(['Country', 'Year'])

# Store results
test_results = []
residuals_by_model = {}

# ==========================================
# 3. RUN TESTS FOR EACH MODEL
# ==========================================
for model_id, model_info in models.items():
    print("\n" + "=" * 80)
    print(f"{model_id}: {model_info['name']}")
    print("=" * 80)
    
    # Prepare data
    exog_vars = model_info['vars']
    exog = df[exog_vars]
    endog = df['ln_arrivals']
    
    # Run regression with entity fixed effects
    mod = PanelOLS(endog, exog, entity_effects=True)
    res = mod.fit(cov_type='clustered', cluster_entity=True)
    
    # Get residuals
    residuals = res.resids
    residuals_df = residuals.reset_index()
    residuals_df.columns = ['Country', 'Year', 'residual']
    residuals_by_model[model_id] = residuals_df
    
    # ==========================================
    # TEST 1: MODIFIED WALD TEST FOR HETEROSKEDASTICITY
    # ==========================================
    print("\n" + "-" * 80)
    print("Modified Wald Test for Groupwise Heteroskedasticity")
    print("-" * 80)
    print("H₀: σ²ᵢ = σ² for all i (homoskedasticity)")
    print("H₁: σ²ᵢ ≠ σ² for at least one i (heteroskedasticity)")
    print()
    
    # Calculate residual variance for each country
    country_variances = {}
    for country in residuals_df['Country'].unique():
        country_resids = residuals_df[residuals_df['Country'] == country]['residual']
        country_variances[country] = np.var(country_resids, ddof=1)
    
    # Modified Wald statistic
    # W = Σ nᵢ * (ln(σ̂²) - ln(σ̂ᵢ²))² where σ̂² is pooled variance
    n_countries = len(country_variances)
    pooled_var = np.var(residuals_df['residual'], ddof=1)
    
    wald_stat = 0
    for country, var in country_variances.items():
        n_i = len(residuals_df[residuals_df['Country'] == country])
        if var > 0:  # Avoid log(0)
            wald_stat += n_i * (np.log(pooled_var) - np.log(var)) ** 2
    
    # Chi-squared distribution with (n_countries - 1) degrees of freedom
    df_wald = n_countries - 1
    p_value_wald = 1 - stats.chi2.cdf(wald_stat, df_wald)
    
    print(f"Test Statistic: χ² = {wald_stat:.4f}")
    print(f"Degrees of Freedom: {df_wald}")
    print(f"P-value: {p_value_wald:.6f}")
    
    if p_value_wald < 0.01:
        print("Result: ❌ REJECT H₀ at 1% level")
        print("Interpretation: Strong evidence of heteroskedasticity across countries.")
        wald_result = "Reject H₀"
    elif p_value_wald < 0.05:
        print("Result: ⚠️  REJECT H₀ at 5% level")
        print("Interpretation: Evidence of heteroskedasticity across countries.")
        wald_result = "Reject H₀"
    else:
        print("Result: ✓ FAIL TO REJECT H₀")
        print("Interpretation: No strong evidence of heteroskedasticity.")
        wald_result = "Fail to reject H₀"
    
    print("\nCountry-specific residual variances:")
    for country, var in sorted(country_variances.items(), key=lambda x: x[1], reverse=True):
        print(f"  {country:15s}: σ² = {var:.4f}")
    
    # ==========================================
    # TEST 2: WOOLDRIDGE TEST FOR AUTOCORRELATION
    # ==========================================
    print("\n" + "-" * 80)
    print("Wooldridge Test for Autocorrelation in Panel Data")
    print("-" * 80)
    print("H₀: No first-order autocorrelation")
    print("H₁: First-order autocorrelation exists")
    print()
    
    # Wooldridge test: regress Δresidual on lagged residual
    # For each country, calculate first differences and lag
    wooldridge_data = []
    
    for country in residuals_df['Country'].unique():
        country_data = residuals_df[residuals_df['Country'] == country].sort_values('Year')
        
        if len(country_data) > 2:  # Need at least 3 observations
            resids = country_data['residual'].values
            
            # First differences: Δe_t = e_t - e_{t-1}
            delta_resids = np.diff(resids)
            
            # Lagged residuals: e_{t-1}
            lagged_resids = resids[:-1]
            
            for i in range(len(delta_resids)):
                wooldridge_data.append({
                    'country': country,
                    'delta_resid': delta_resids[i],
                    'lagged_resid': lagged_resids[i]
                })
    
    wooldridge_df = pd.DataFrame(wooldridge_data)
    
    # Run regression: Δe_t = α + β*e_{t-1} + u_t
    # Test H₀: β = -0.5 (no autocorrelation)
    from scipy.stats import linregress
    
    if len(wooldridge_df) > 0:
        slope, intercept, r_value, p_value_wool, std_err = linregress(
            wooldridge_df['lagged_resid'], 
            wooldridge_df['delta_resid']
        )
        
        # Calculate t-statistic for H₀: β = -0.5
        t_stat = (slope - (-0.5)) / std_err
        df_wool = len(wooldridge_df) - 2
        p_value_wool_adjusted = 2 * (1 - stats.t.cdf(abs(t_stat), df_wool))
        
        # Also calculate F-statistic (more common in Wooldridge test)
        f_stat = t_stat ** 2
        p_value_f = 1 - stats.f.cdf(f_stat, 1, df_wool)
        
        print(f"Regression coefficient: β = {slope:.4f} (SE = {std_err:.4f})")
        print(f"F-statistic: F(1, {df_wool}) = {f_stat:.4f}")
        print(f"P-value: {p_value_f:.6f}")
        
        if p_value_f < 0.01:
            print("Result: ❌ REJECT H₀ at 1% level")
            print("Interpretation: Strong evidence of first-order autocorrelation.")
            wool_result = "Reject H₀"
        elif p_value_f < 0.05:
            print("Result: ⚠️  REJECT H₀ at 5% level")
            print("Interpretation: Evidence of first-order autocorrelation.")
            wool_result = "Reject H₀"
        else:
            print("Result: ✓ FAIL TO REJECT H₀")
            print("Interpretation: No strong evidence of autocorrelation.")
            wool_result = "Fail to reject H₀"
    else:
        print("⚠️  Insufficient data for Wooldridge test")
        f_stat = np.nan
        p_value_f = np.nan
        wool_result = "N/A"
    
    # Store results
    test_results.append({
        'Model': model_id,
        'Model_Name': model_info['name'],
        'Wald_Statistic': wald_stat,
        'Wald_DF': df_wald,
        'Wald_PValue': p_value_wald,
        'Wald_Result': wald_result,
        'Wooldridge_F': f_stat,
        'Wooldridge_PValue': p_value_f,
        'Wooldridge_Result': wool_result
    })

# ==========================================
# 4. SAVE RESULTS TO CSV
# ==========================================
results_df = pd.DataFrame(test_results)
results_df.to_csv(os.path.join(script_dir, 'heteroskedasticity_autocorrelation_results.csv'), index=False)
print("\n" + "=" * 80)
print("✓ Results saved to: heteroskedasticity_autocorrelation_results.csv")

# ==========================================
# 5. CREATE VISUALIZATIONS
# ==========================================
print("\nCreating visualizations...")

# Figure 1: Residual variance by country for each model
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, (model_id, model_info) in enumerate(models.items()):
    ax = axes[idx]
    residuals_df = residuals_by_model[model_id]
    
    # Calculate variance for each country
    country_vars = residuals_df.groupby('Country')['residual'].var().sort_values(ascending=False)
    
    # Bar plot
    colors = ['#dc2626' if var > country_vars.median() * 1.5 else '#3b82f6' for var in country_vars]
    ax.bar(range(len(country_vars)), country_vars.values, color=colors)
    ax.set_xticks(range(len(country_vars)))
    ax.set_xticklabels(country_vars.index, rotation=45, ha='right')
    ax.set_ylabel('Residual Variance (σ²)', fontsize=11, fontweight='bold')
    ax.set_title(f'{model_id}: {model_info["name"]}\nResidual Variance by Country', 
                 fontsize=12, fontweight='bold')
    ax.axhline(y=country_vars.median(), color='orange', linestyle='--', 
               linewidth=2, label=f'Median = {country_vars.median():.4f}')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'residual_variance_by_country.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: residual_variance_by_country.png")

# Figure 2: Test statistics comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Wald test p-values
models_short = [r['Model'] for r in test_results]
wald_pvals = [r['Wald_PValue'] for r in test_results]
wool_pvals = [r['Wooldridge_PValue'] for r in test_results]

# Plot 1: Wald test
colors_wald = ['#dc2626' if p < 0.05 else '#16a34a' for p in wald_pvals]
ax1.bar(models_short, wald_pvals, color=colors_wald)
ax1.axhline(y=0.05, color='orange', linestyle='--', linewidth=2, label='α = 0.05')
ax1.axhline(y=0.01, color='red', linestyle='--', linewidth=2, label='α = 0.01')
ax1.set_ylabel('P-value', fontsize=12, fontweight='bold')
ax1.set_title('Modified Wald Test for Heteroskedasticity\n(Lower p-value = More heteroskedasticity)', 
              fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, max(wald_pvals) * 1.1)

# Plot 2: Wooldridge test
colors_wool = ['#dc2626' if p < 0.05 else '#16a34a' for p in wool_pvals if not np.isnan(p)]
ax2.bar(models_short, wool_pvals, color=colors_wool)
ax2.axhline(y=0.05, color='orange', linestyle='--', linewidth=2, label='α = 0.05')
ax2.axhline(y=0.01, color='red', linestyle='--', linewidth=2, label='α = 0.01')
ax2.set_ylabel('P-value', fontsize=12, fontweight='bold')
ax2.set_title('Wooldridge Test for Autocorrelation\n(Lower p-value = More autocorrelation)', 
              fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)
ax2.set_ylim(0, max([p for p in wool_pvals if not np.isnan(p)]) * 1.1)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'diagnostic_test_pvalues.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: diagnostic_test_pvalues.png")

# Figure 3: Residual plots for Model F (most complex model)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

model_f_resids = residuals_by_model['Model F']

# Plot 1: Residuals over time
ax = axes[0, 0]
for country in model_f_resids['Country'].unique():
    country_data = model_f_resids[model_f_resids['Country'] == country]
    ax.plot(country_data['Year'], country_data['residual'], marker='o', label=country, alpha=0.7)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.set_xlabel('Year', fontsize=11, fontweight='bold')
ax.set_ylabel('Residual', fontsize=11, fontweight='bold')
ax.set_title('Residuals Over Time (Model F)', fontsize=12, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.grid(alpha=0.3)

# Plot 2: Residual distribution
ax = axes[0, 1]
ax.hist(model_f_resids['residual'], bins=20, color='#3b82f6', alpha=0.7, edgecolor='black')
ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax.set_xlabel('Residual', fontsize=11, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax.set_title('Residual Distribution (Model F)', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Plot 3: Q-Q plot
ax = axes[1, 0]
stats.probplot(model_f_resids['residual'], dist="norm", plot=ax)
ax.set_title('Q-Q Plot (Model F)', fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)

# Plot 4: Residuals by country (boxplot)
ax = axes[1, 1]
country_resids = [model_f_resids[model_f_resids['Country'] == c]['residual'].values 
                  for c in sorted(model_f_resids['Country'].unique())]
bp = ax.boxplot(country_resids, labels=sorted(model_f_resids['Country'].unique()), patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#3b82f6')
    patch.set_alpha(0.7)
ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax.set_xticklabels(sorted(model_f_resids['Country'].unique()), rotation=45, ha='right')
ax.set_ylabel('Residual', fontsize=11, fontweight='bold')
ax.set_title('Residuals by Country (Model F)', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'residual_diagnostics_model_f.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: residual_diagnostics_model_f.png")

# ==========================================
# 6. CREATE SUMMARY REPORT
# ==========================================
summary_lines = []
summary_lines.append("=" * 80)
summary_lines.append("HETEROSKEDASTICITY AND AUTOCORRELATION TEST SUMMARY")
summary_lines.append("=" * 80)
summary_lines.append(f"Dataset: {len(df)} observations, {df.index.get_level_values('Country').nunique()} countries")
summary_lines.append(f"Years: {df.index.get_level_values('Year').min()}-{df.index.get_level_values('Year').max()}")
summary_lines.append("")

for result in test_results:
    summary_lines.append(f"\n{result['Model']}: {result['Model_Name']}")
    summary_lines.append("-" * 80)
    
    # Wald test
    summary_lines.append("\nModified Wald Test for Heteroskedasticity:")
    summary_lines.append(f"  Test Statistic: χ²({result['Wald_DF']}) = {result['Wald_Statistic']:.4f}")
    summary_lines.append(f"  P-value: {result['Wald_PValue']:.6f}")
    summary_lines.append(f"  Result: {result['Wald_Result']}")
    
    if result['Wald_PValue'] < 0.05:
        summary_lines.append("  ⚠️  Evidence of heteroskedasticity - use robust standard errors")
    else:
        summary_lines.append("  ✓ No strong evidence of heteroskedasticity")
    
    # Wooldridge test
    summary_lines.append("\nWooldridge Test for Autocorrelation:")
    if not np.isnan(result['Wooldridge_F']):
        summary_lines.append(f"  F-statistic: {result['Wooldridge_F']:.4f}")
        summary_lines.append(f"  P-value: {result['Wooldridge_PValue']:.6f}")
        summary_lines.append(f"  Result: {result['Wooldridge_Result']}")
        
        if result['Wooldridge_PValue'] < 0.05:
            summary_lines.append("  ⚠️  Evidence of autocorrelation - consider AR(1) correction or year FE")
        else:
            summary_lines.append("  ✓ No strong evidence of autocorrelation")
    else:
        summary_lines.append("  N/A - Insufficient data")

summary_lines.append("\n" + "=" * 80)
summary_lines.append("INTERPRETATION AND RECOMMENDATIONS")
summary_lines.append("=" * 80)
summary_lines.append("""
Modified Wald Test:
- Tests whether residual variance differs across countries (heteroskedasticity)
- Rejection of H₀ indicates country-specific variance
- Solution: Use clustered/robust standard errors (which we do)

Wooldridge Test:
- Tests for first-order autocorrelation in panel data
- Rejection of H₀ indicates errors are correlated over time
- Solutions: (1) Include year fixed effects, (2) Use AR(1) correction, (3) Cluster by time

Our Approach:
- We use clustered standard errors (by country) to address heteroskedasticity
- We include year fixed effects in some specifications to capture temporal patterns
- These adjustments make our inference robust to both issues
""")

summary_text = "\n".join(summary_lines)
print("\n" + summary_text)

# Save summary
with open(os.path.join(script_dir, 'heteroskedasticity_autocorrelation_summary.txt'), 'w') as f:
    f.write(summary_text)

print(f"\n✓ Summary saved to: heteroskedasticity_autocorrelation_summary.txt")

print("\n" + "=" * 80)
print("DIAGNOSTICS COMPLETE")
print("=" * 80)
print("Generated files:")
print("  1. heteroskedasticity_autocorrelation_results.csv - Test statistics")
print("  2. residual_variance_by_country.png - Variance comparison")
print("  3. diagnostic_test_pvalues.png - P-value comparison")
print("  4. residual_diagnostics_model_f.png - Detailed residual plots")
print("  5. heteroskedasticity_autocorrelation_summary.txt - Full report")
