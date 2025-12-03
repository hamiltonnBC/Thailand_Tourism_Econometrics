import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD YOUR DATA
# ==========================================
df = pd.read_csv('/Users/hamiltonn/repos/Thailand_Tourism_Econometrics/final_regressions/Primary_Dataset_For_Panel_FINAL.csv')

# ==========================================
# 2. FILTER DATA FOR MODEL 1 SPECIFICATION
# ==========================================
# Countries: Exclude Korea, Philippines, United Kingdom (missing recent data)
countries_to_include = ['Australia', 'Cambodia', 'Indonesia', 'Japan', 
                        'Malaysia', 'Maldives', 'Singapore', 'Thailand', 'Viet Nam']

# Years: 2008-2024 (when peace_index becomes available)
df = df[(df['Country'].isin(countries_to_include)) & 
        (df['Year'] >= 2008) & 
        (df['Year'] <= 2024)]

# Drop rows with missing values in key variables
df = df.dropna(subset=['arrivals_from_china', 'peace_index', 'cpi_index', 
                       'gdp_china', 'exchange_rate'])

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
df['ln_cpi'] = np.log(df['cpi_index'])
df['ln_gdp_china'] = np.log(df['gdp_china'])
df['ln_exchange_rate'] = np.log(df['exchange_rate'])
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
          'ln_exchange_rate', 'covid_dummy', 'post_covid']].describe())

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

# Model Comparison
print("\n" + "=" * 80)
print("MODEL COMPARISON")
print("=" * 80)
comparison = pd.DataFrame({
    'Model A (COVID Dummy)': [res_a.rsquared, res_a.rsquared_within, res_a.f_statistic.stat, res_a.nobs],
    'Model B (Time FE)': [res_b.rsquared, res_b.rsquared_within, res_b.f_statistic.stat, res_b.nobs],
    'Model C (Thailand Asymmetry)': [res_c.rsquared, res_c.rsquared_within, res_c.f_statistic.stat, res_c.nobs]
}, index=['R-squared', 'R-squared Within', 'F-statistic', 'N Observations'])
print(comparison)

# ==========================================
# 7. SAVE RESULTS
# ==========================================
# Save regression results to text file
with open('regression_results_model1.txt', 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("GRAVITY PANEL REGRESSION RESULTS (2008-2024)\n")
    f.write("=" * 80 + "\n\n")
    f.write("MODEL A: Entity FE + COVID Dummy\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_a) + "\n\n")
    f.write("MODEL B: Entity FE + Time FE\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_b) + "\n\n")
    f.write("MODEL C: Thailand Asymmetry\n")
    f.write("-" * 80 + "\n")
    f.write(str(res_c) + "\n")

print("\n✓ Results saved to 'regression_results_model1.txt'")

# Save coefficients to CSV for easy import to Excel/LaTeX
coef_comparison = pd.DataFrame({
    'Model_A_Coef': res_a.params,
    'Model_A_SE': res_a.std_errors,
    'Model_A_Pval': res_a.pvalues,
    'Model_B_Coef': res_b.params,
    'Model_B_SE': res_b.std_errors,
    'Model_B_Pval': res_b.pvalues,
    'Model_C_Coef': res_c.params,
    'Model_C_SE': res_c.std_errors,
    'Model_C_Pval': res_c.pvalues
})
coef_comparison.to_csv('regression_coefficients_model1.csv')
print("✓ Coefficients saved to 'regression_coefficients_model1.csv'")

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
plt.savefig('arrivals_by_country.png', dpi=300, bbox_inches='tight')
print("✓ Saved: arrivals_by_country.png")
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
plt.savefig('thailand_asymmetry.png', dpi=300, bbox_inches='tight')
print("✓ Saved: thailand_asymmetry.png")
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
plt.savefig('log_arrivals_by_country.png', dpi=300, bbox_inches='tight')
print("✓ Saved: log_arrivals_by_country.png")
plt.close()

# Plot 4: Correlation Heatmap
plt.figure(figsize=(10, 8))
corr_vars = ['ln_arrivals', 'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate']
correlation_matrix = df_plot[corr_vars].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Saved: correlation_matrix.png")
plt.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nFiles Generated:")
print("  1. regression_results_model1.txt - Full regression output")
print("  2. regression_coefficients_model1.csv - Coefficients table")
print("  3. arrivals_by_country.png - Time series by country")
print("  4. thailand_asymmetry.png - Thailand vs others comparison")
print("  5. log_arrivals_by_country.png - Log-transformed arrivals")
print("  6. correlation_matrix.png - Variable correlations")
print("\nKey Finding:")
if 'thailand_post_covid' in params_c.index:
    if params_c['thailand_post_covid'] < 0:
        print(f"  → Thailand shows a {abs(params_c['thailand_post_covid']*100):.2f}% SLOWER recovery than other countries")
    else:
        print(f"  → Thailand shows a {params_c['thailand_post_covid']*100:.2f}% FASTER recovery than other countries")
print("=" * 80)
