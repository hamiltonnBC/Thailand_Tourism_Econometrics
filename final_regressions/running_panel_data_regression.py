import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# 1. LOAD YOUR DATA
# ==========================================
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'Primary_Dataset_For_Panel_FINAL.csv')
df = pd.read_csv(data_path)

# ==========================================
# 2. FILTER DATA FOR MODEL 1 SPECIFICATION
# ==========================================
# Countries: Exclude Korea, Philippines, United Kingdom (missing recent data)
# Also excluding Cambodia and Indonesia for this analysis
countries_to_include = ['Australia', 'Japan', 
                        'Malaysia', 'Maldives', 'Singapore', 'Thailand', 'Viet Nam']

# Years: 2008-2024 (when peace_index becomes available)
df = df[(df['Country'].isin(countries_to_include)) & 
        (df['Year'] >= 2008) & 
        (df['Year'] <= 2024)]

print('oof')
# Drop rows with missing values in key variables
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'CPI_destination', 
                       'gdp_china', 'exchange_rate', 'RER'])

print("=" * 80)
print("MODEL 1: GRAVITY PANEL ANALYSIS (2008-2024)")
print("=" * 80)
print(f"Loaded {len(df)} observations across {df['Country'].nunique()} countries")
print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
print(f"Countries: {sorted(df['Country'].unique())}")
print(f"\nObservations per country:")
print(df.groupby('Country').size().sort_values(ascending=False))


# ==========================================
# 3. FEATURE ENGINEERING (Crucial Step)
# ==========================================

# A. Log Transformations (for Gravity Model interpretation as elasticities)
# Log both dependent and independent variables for elasticity interpretation
df['ln_arrivals'] = np.log(df['arrivals_from_china'])
df['ln_cpi'] = np.log(df['CPI_destination'])
df['ln_gdp_china'] = np.log(df['gdp_china'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])

# Check RER values before log transformation
print("\n" + "=" * 80)
print("RER DATA DIAGNOSTICS")
print("=" * 80)
print(f"RER range: {df['RER'].min():.6f} to {df['RER'].max():.6f}")
print(f"RER mean: {df['RER'].mean():.6f}")
print(f"RER median: {df['RER'].median():.6f}")
print(f"Values < 0.01: {(df['RER'] < 0.01).sum()} observations")
print(f"Values > 10: {(df['RER'] > 10).sum()} observations")

# SOLUTION: Normalize RER within each country (country-specific scaling)
# This removes the arbitrary currency scale differences while preserving time variation
# Formula: RER_normalized = RER / mean(RER) for each country
# This makes the mean RER = 1 for each country, so log(1) = 0 at the mean
df['RER_normalized'] = df.groupby('Country')['RER'].transform(lambda x: x / x.mean())

print(f"\nAfter normalization (country-specific):")
print(f"RER_normalized range: {df['RER_normalized'].min():.6f} to {df['RER_normalized'].max():.6f}")
print(f"RER_normalized mean: {df['RER_normalized'].mean():.6f}")

# Log transform the NORMALIZED RER (much more stable)
df['ln_rer'] = np.log(df['RER_normalized'])

# Check for problematic log values
print(f"\nln_rer range: {df['ln_rer'].min():.2f} to {df['ln_rer'].max():.2f}")
print(f"Extreme negative ln_rer (< -5): {(df['ln_rer'] < -5).sum()} observations")
print(f"\nInterpretation: ln_rer now measures % deviation from country-specific mean RER")

# Peace index stays in levels (it's already an index)

# B. Create COVID Dummy Variable
# COVID-19 impact period: 2020-2021 (strict lockdowns, travel restrictions)
df['covid_dummy'] = ((df['Year'] >= 2020) & (df['Year'] <= 2021)).astype(int)

# C. Create Post-COVID Recovery Dummy (2022-2024)
# To capture asymmetric recovery patterns
df['post_covid'] = (df['Year'] >= 2022).astype(int)

# D. Create the "Thailand Asymmetry" Interaction Term
# This captures if Thailand's recovery is different from other countries
df['is_thailand'] = (df['Country'] == 'Thailand').astype(int)
df['thailand_post_covid'] = df['is_thailand'] * df['post_covid']

# E. Time trend variable (for robustness checks)
df['time_trend'] = df['Year'] - df['Year'].min()

print("\n" + "=" * 80)
print("VARIABLE SUMMARY STATISTICS")
print("=" * 80)
print(df[['ln_arrivals', 'peace_index', 'ln_cpi', 'ln_gdp_china', 
          'ln_exchange_rate', 'ln_rer', 'covid_dummy', 'post_covid']].describe())

# ==========================================
# 4. SET UP PANEL DATA STRUCTURE
# ==========================================
# Panel data must have a MultiIndex: (Entity, Time)
df = df.set_index(['Country', 'Year'])

# ==========================================
# 5. RUN MULTIPLE MODEL SPECIFICATIONS
# ==========================================

print("\n" + "=" * 80)
print("REGRESSION RESULTS")
print("=" * 80)

# MODEL A: Baseline Gravity Model with Entity FE + COVID Dummy
print("\n" + "-" * 80)
print("MODEL A: Entity Fixed Effects + COVID Dummy")
print("-" * 80)
exog_vars_a = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 'covid_dummy']
exog_a = sm.add_constant(df[exog_vars_a])
mod_a = PanelOLS(df['ln_arrivals'], exog_a, entity_effects=True, time_effects=False)
res_a = mod_a.fit(cov_type='clustered', cluster_entity=True)
print(res_a)

# MODEL B: Entity FE + Time FE (absorbs COVID and all time-varying shocks)
# Note: gdp_china is dropped because it's absorbed by time FE (same for all countries each year)
print("\n" + "-" * 80)
print("MODEL B: Entity Fixed Effects + Time Fixed Effects")
print("(Note: gdp_china excluded - absorbed by time FE)")
print("-" * 80)
exog_vars_b = ['peace_index', 'ln_cpi', 'ln_exchange_rate']
exog_b = df[exog_vars_b]  # No constant needed with both FE
mod_b = PanelOLS(df['ln_arrivals'], exog_b, entity_effects=True, time_effects=True)
res_b = mod_b.fit(cov_type='clustered', cluster_entity=True)
print(res_b)

# MODEL C: Thailand Asymmetry Model (Entity FE + COVID + Thailand Post-COVID Interaction)
print("\n" + "-" * 80)
print("MODEL C: Thailand Asymmetry Analysis (Entity FE + COVID + Thailand Interaction)")
print("-" * 80)
exog_vars_c = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 
               'covid_dummy', 'post_covid', 'thailand_post_covid']
exog_c = sm.add_constant(df[exog_vars_c])
mod_c = PanelOLS(df['ln_arrivals'], exog_c, entity_effects=True, time_effects=False)
res_c = mod_c.fit(cov_type='clustered', cluster_entity=True)
print(res_c)

# MODEL D: RER Instead of Nominal Exchange Rate (Entity FE + COVID)
print("\n" + "-" * 80)
print("MODEL D: Real Exchange Rate (RER) - Entity FE + COVID Dummy")
print("-" * 80)
try:
    exog_vars_d = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 'covid_dummy']
    exog_d = sm.add_constant(df[exog_vars_d])
    mod_d = PanelOLS(df['ln_arrivals'], exog_d, entity_effects=True, time_effects=False)
    res_d = mod_d.fit(cov_type='clustered', cluster_entity=True)
    print(res_d)
    model_d_success = True
except Exception as e:
    print(f"MODEL D FAILED: {str(e)}")
    res_d = None
    model_d_success = False

# MODEL E: RER with Time FE
print("\n" + "-" * 80)
print("MODEL E: Real Exchange Rate (RER) - Entity FE + Time FE")
print("(Note: gdp_china excluded - absorbed by time FE)")
print("-" * 80)
try:
    exog_vars_e = ['peace_index', 'ln_cpi', 'ln_rer']
    exog_e = df[exog_vars_e]
    mod_e = PanelOLS(df['ln_arrivals'], exog_e, entity_effects=True, time_effects=True)
    res_e = mod_e.fit(cov_type='clustered', cluster_entity=True)
    print(res_e)
    model_e_success = True
except Exception as e:
    print(f"MODEL E FAILED: {str(e)}")
    res_e = None
    model_e_success = False

# MODEL F: RER with Thailand Asymmetry
print("\n" + "-" * 80)
print("MODEL F: RER + Thailand Asymmetry Analysis")
print("-" * 80)
try:
    exog_vars_f = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 
                   'covid_dummy', 'post_covid', 'thailand_post_covid']
    exog_f = sm.add_constant(df[exog_vars_f])
    mod_f = PanelOLS(df['ln_arrivals'], exog_f, entity_effects=True, time_effects=False)
    res_f = mod_f.fit(cov_type='clustered', cluster_entity=True)
    print(res_f)
    model_f_success = True
except Exception as e:
    print(f"MODEL F FAILED: {str(e)}")
    res_f = None
    model_f_success = False

# MODEL G: Both Nominal and Real Exchange Rates (Horse Race)
print("\n" + "-" * 80)
print("MODEL G: Nominal vs Real Exchange Rate Comparison (Entity FE + COVID)")
print("-" * 80)
try:
    exog_vars_g = ['peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 'ln_rer', 'covid_dummy']
    exog_g = sm.add_constant(df[exog_vars_g])
    
    # Check for infinite or NaN values
    if exog_g.isin([np.inf, -np.inf]).any().any():
        print("WARNING: Infinite values detected in exogenous variables")
        print(exog_g.isin([np.inf, -np.inf]).sum())
    
    mod_g = PanelOLS(df['ln_arrivals'], exog_g, entity_effects=True, time_effects=False)
    res_g = mod_g.fit(cov_type='clustered', cluster_entity=True)
    print(res_g)
except Exception as e:
    print(f"MODEL G FAILED: {str(e)}")
    print("Skipping Model G due to numerical issues (likely multicollinearity between nominal and real ER)")
    # Create a dummy result for Model G
    res_g = res_d  # Use Model D as placeholder

# ==========================================
# 6. INTERPRETATION & DIAGNOSTICS
# ==========================================
print("\n" + "=" * 80)
print("MODEL INTERPRETATION")
print("=" * 80)

print("\n--- MODEL A: Baseline Gravity Model ---")
params_a = res_a.params
print(f"Peace Index: 1 unit increase → {params_a['peace_index']*100:.2f}% change in arrivals")
print(f"CPI: 1% increase → {params_a['ln_cpi']:.3f}% change in arrivals")
print(f"China GDP: 1% increase → {params_a['ln_gdp_china']:.3f}% change in arrivals")
print(f"Exchange Rate: 1% appreciation → {params_a['ln_exchange_rate']:.3f}% change in arrivals")
print(f"COVID Impact: {params_a['covid_dummy']*100:.2f}% change during 2020-2021")

print("\n--- MODEL C: Thailand Asymmetry ---")
params_c = res_c.params
print(f"Post-COVID Recovery (all countries): {params_c['post_covid']*100:.2f}% change")
print(f"Thailand-Specific Post-COVID Effect: {params_c['thailand_post_covid']*100:.2f}% ADDITIONAL change")
print(f"Total Thailand Post-COVID Effect: {(params_c['post_covid'] + params_c['thailand_post_covid'])*100:.2f}%")

if model_d_success and res_d is not None:
    print("\n--- MODEL D: Real Exchange Rate (RER) ---")
    params_d = res_d.params
    print(f"Peace Index: 1 unit increase → {params_d['peace_index']*100:.2f}% change in arrivals")
    print(f"CPI: 1% increase → {params_d['ln_cpi']:.3f}% change in arrivals")
    print(f"China GDP: 1% increase → {params_d['ln_gdp_china']:.3f}% change in arrivals")
    print(f"Real Exchange Rate (RER): 1% appreciation → {params_d['ln_rer']:.3f}% change in arrivals")
    print(f"COVID Impact: {params_d['covid_dummy']*100:.2f}% change during 2020-2021")

if model_f_success and res_f is not None:
    print("\n--- MODEL F: RER + Thailand Asymmetry ---")
    params_f = res_f.params
    print(f"Real Exchange Rate (RER): 1% appreciation → {params_f['ln_rer']:.3f}% change in arrivals")
    print(f"Post-COVID Recovery (all countries): {params_f['post_covid']*100:.2f}% change")
    print(f"Thailand-Specific Post-COVID Effect: {params_f['thailand_post_covid']*100:.2f}% ADDITIONAL change")
    print(f"Total Thailand Post-COVID Effect: {(params_f['post_covid'] + params_f['thailand_post_covid'])*100:.2f}%")

# Model Comparison
print("\n" + "=" * 80)
print("MODEL COMPARISON")
print("=" * 80)

comparison_data = {
    'Model A (Nominal ER)': [res_a.rsquared, res_a.rsquared_within, res_a.f_statistic.stat, res_a.nobs],
    'Model B (Time FE)': [res_b.rsquared, res_b.rsquared_within, res_b.f_statistic.stat, res_b.nobs],
    'Model C (Thailand)': [res_c.rsquared, res_c.rsquared_within, res_c.f_statistic.stat, res_c.nobs]
}

if model_d_success and res_d is not None:
    comparison_data['Model D (RER)'] = [res_d.rsquared, res_d.rsquared_within, res_d.f_statistic.stat, res_d.nobs]
if model_e_success and res_e is not None:
    comparison_data['Model E (RER+Time FE)'] = [res_e.rsquared, res_e.rsquared_within, res_e.f_statistic.stat, res_e.nobs]
if model_f_success and res_f is not None:
    comparison_data['Model F (RER+Thailand)'] = [res_f.rsquared, res_f.rsquared_within, res_f.f_statistic.stat, res_f.nobs]

comparison = pd.DataFrame(comparison_data, 
                         index=['R-squared', 'R-squared Within', 'F-statistic', 'N Observations'])
print(comparison)

# ==========================================
# 7. SAVE RESULTS
# ==========================================
# Save regression results to text file
with open(os.path.join(script_dir, 'regression_results_model1_woCandE.txt'), 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("GRAVITY PANEL REGRESSION RESULTS (2008-2024)\n")
    f.write("=" * 80 + "\n\n")
    f.write("MODEL A: Entity FE + COVID Dummy (Nominal ER)\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_a) + "\n\n")
    f.write("MODEL B: Entity FE + Time FE (Nominal ER)\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_b) + "\n\n")
    f.write("MODEL C: Thailand Asymmetry (Nominal ER)\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_c) + "\n\n")
    
    if model_d_success and res_d is not None:
        f.write("MODEL D: Entity FE + COVID Dummy (RER)\n")
        f.write("-" * 80 + "\n")
        f.write(str(res_d) + "\n\n")
    
    if model_e_success and res_e is not None:
        f.write("MODEL E: Entity FE + Time FE (RER)\n")
        f.write("-" * 80 + "\n")
        f.write(str(res_e) + "\n\n")
    
    if model_f_success and res_f is not None:
        f.write("MODEL F: Thailand Asymmetry (RER)\n")
        f.write("-" * 80 + "\n")
        f.write(str(res_f) + "\n\n")

print("\n✓ Results saved to 'regression_results_model1_woCandE.txt'")

# Save coefficients to CSV for easy import to Excel/LaTeX
# Combine all model results
params_data = {
    'Model_A_Coef': res_a.params,
    'Model_A_SE': res_a.std_errors,
    'Model_A_Pval': res_a.pvalues,
    'Model_B_Coef': res_b.params,
    'Model_B_SE': res_b.std_errors,
    'Model_B_Pval': res_b.pvalues,
    'Model_C_Coef': res_c.params,
    'Model_C_SE': res_c.std_errors,
    'Model_C_Pval': res_c.pvalues
}

if model_d_success and res_d is not None:
    params_data.update({
        'Model_D_Coef': res_d.params,
        'Model_D_SE': res_d.std_errors,
        'Model_D_Pval': res_d.pvalues
    })
if model_e_success and res_e is not None:
    params_data.update({
        'Model_E_Coef': res_e.params,
        'Model_E_SE': res_e.std_errors,
        'Model_E_Pval': res_e.pvalues
    })
if model_f_success and res_f is not None:
    params_data.update({
        'Model_F_Coef': res_f.params,
        'Model_F_SE': res_f.std_errors,
        'Model_F_Pval': res_f.pvalues
    })

all_params = pd.DataFrame(params_data)
all_params.to_csv(os.path.join(script_dir, 'regression_coefficients_model1_woCandE.csv'))
print("✓ Coefficients saved to 'regression_coefficients_model1_woCandE.csv'")

# ==========================================
# 8. VISUALIZATIONS
# ==========================================
print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Reset index for plotting
df_plot = df.reset_index()

# Plot 1: Tourist Arrivals Over Time by Country
plt.figure(figsize=(14, 8))
for country in df_plot['Country'].unique():
    country_data = df_plot[df_plot['Country'] == country]
    plt.plot(country_data['Year'], country_data['arrivals_from_china'], 
             marker='o', label=country, linewidth=2)

plt.axvline(x=2020, color='red', linestyle='--', linewidth=2, label='COVID-19', alpha=0.7)
plt.axvline(x=2022, color='green', linestyle='--', linewidth=2, label='Post-COVID', alpha=0.7)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Chinese Tourist Arrivals', fontsize=12)
plt.title('Chinese Tourist Arrivals by Destination (2008-2024)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'arrivals_by_country_woCandE.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: arrivals_by_country_woCandE.png")
plt.close()

# Plot 2: Thailand vs Others - Recovery Pattern
plt.figure(figsize=(12, 6))
thailand_data = df_plot[df_plot['Country'] == 'Thailand']
others_data = df_plot[df_plot['Country'] != 'Thailand'].groupby('Year')['arrivals_from_china'].mean().reset_index()

plt.plot(thailand_data['Year'], thailand_data['arrivals_from_china'], 
         marker='o', linewidth=3, label='Thailand', color='#FF6B6B')
plt.plot(others_data['Year'], others_data['arrivals_from_china'], 
         marker='s', linewidth=3, label='Other Countries (Average)', color='#4ECDC4')

plt.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.5)
plt.axvline(x=2022, color='green', linestyle='--', linewidth=2, alpha=0.5)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Chinese Tourist Arrivals', fontsize=12)
plt.title('Thailand vs Other Destinations: Recovery Asymmetry', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'thailand_asymmetry_woCandE.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: thailand_asymmetry_woCandE.png")
plt.close()

# Plot 3: Log Arrivals (normalized view)
plt.figure(figsize=(14, 8))
for country in df_plot['Country'].unique():
    country_data = df_plot[df_plot['Country'] == country]
    plt.plot(country_data['Year'], country_data['ln_arrivals'], 
             marker='o', label=country, linewidth=2)

plt.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.7)
plt.axvline(x=2022, color='green', linestyle='--', linewidth=2, alpha=0.7)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Log(Chinese Tourist Arrivals)', fontsize=12)
plt.title('Log-Transformed Tourist Arrivals (2008-2024)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'log_arrivals_by_country_woCandE.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: log_arrivals_by_country_woCandE.png")
plt.close()

# Plot 4: Correlation Heatmap
plt.figure(figsize=(10, 8))
corr_vars = ['ln_arrivals', 'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 'ln_rer']
correlation_matrix = df_plot[corr_vars].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Variables (Including RER)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'correlation_matrix_woCandE.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: correlation_matrix_woCandE.png")
plt.close()

# Plot 5: Nominal vs Real Exchange Rate Comparison
plt.figure(figsize=(14, 8))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Plot nominal exchange rate
for country in df_plot['Country'].unique():
    country_data = df_plot[df_plot['Country'] == country]
    ax1.plot(country_data['Year'], country_data['ln_exchange_rate'], 
             marker='o', label=country, linewidth=2, alpha=0.7)
ax1.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Log(Nominal Exchange Rate)', fontsize=11)
ax1.set_title('Nominal Exchange Rate Over Time', fontsize=12, fontweight='bold')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)

# Plot real exchange rate
for country in df_plot['Country'].unique():
    country_data = df_plot[df_plot['Country'] == country]
    ax2.plot(country_data['Year'], country_data['ln_rer'], 
             marker='s', label=country, linewidth=2, alpha=0.7)
ax2.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax2.set_xlabel('Year', fontsize=11)
ax2.set_ylabel('Log(Real Exchange Rate)', fontsize=11)
ax2.set_title('Real Exchange Rate (RER) Over Time', fontsize=12, fontweight='bold')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'exchange_rate_comparison.png'), dpi=300, bbox_inches='tight')
print("✓ Saved: exchange_rate_comparison.png")
plt.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nFiles Generated:")
print("  1. regression_results_model1.txt - Full regression output (7 models)")
print("  2. regression_coefficients_model1.csv - Coefficients table (all models)")
print("  3. arrivals_by_country.png - Time series by country")
print("  4. thailand_asymmetry.png - Thailand vs others comparison")
print("  5. log_arrivals_by_country.png - Log-transformed arrivals")
print("  6. correlation_matrix.png - Variable correlations (including RER)")
print("  7. exchange_rate_comparison.png - Nominal vs Real ER comparison")
print("\nKey Findings:")
if 'thailand_post_covid' in params_c.index:
    if params_c['thailand_post_covid'] < 0:
        print(f"  → Thailand shows a {abs(params_c['thailand_post_covid']*100):.2f}% SLOWER recovery (Nominal ER model)")
    else:
        print(f"  → Thailand shows a {params_c['thailand_post_covid']*100:.2f}% FASTER recovery (Nominal ER model)")

if model_f_success and res_f is not None:
    params_f = res_f.params
    if 'thailand_post_covid' in params_f.index:
        if params_f['thailand_post_covid'] < 0:
            print(f"  → Thailand shows a {abs(params_f['thailand_post_covid']*100):.2f}% SLOWER recovery (RER model)")
        else:
            print(f"  → Thailand shows a {params_f['thailand_post_covid']*100:.2f}% FASTER recovery (RER model)")

print("\nModels Successfully Estimated:")
print(f"  → Models A, B, C (Nominal ER): ✓")
if model_d_success:
    print(f"  → Model D (RER): ✓")
else:
    print(f"  → Model D (RER): ✗ (numerical issues)")
if model_e_success:
    print(f"  → Model E (RER + Time FE): ✓")
else:
    print(f"  → Model E (RER + Time FE): ✗ (numerical issues)")
if model_f_success:
    print(f"  → Model F (RER + Thailand): ✓")
else:
    print(f"  → Model F (RER + Thailand): ✗ (numerical issues)")
print("=" * 80)
