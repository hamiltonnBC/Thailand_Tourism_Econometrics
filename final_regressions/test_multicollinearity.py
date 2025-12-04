"""
Multicollinearity Diagnostics for Panel Regression Models

This script calculates:
1. Variance Inflation Factors (VIF) for each model specification
2. Correlation matrices for all variables
3. Condition numbers to detect severe multicollinearity

Output:
- VIF tables (CSV)
- Correlation heatmaps (PNG)
- Diagnostic summary (TXT)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os

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

# Feature engineering (same as main regression)
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
print("MULTICOLLINEARITY DIAGNOSTICS")
print("=" * 80)
print(f"Sample: {len(df)} observations, {df['Country'].nunique()} countries")
print(f"Years: {df['Year'].min()}-{df['Year'].max()}")
print()

# ==========================================
# 2. DEFINE MODEL SPECIFICATIONS
# ==========================================
models = {
    'Model A: Baseline (Nominal ER)': [
        'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 'covid_dummy'
    ],
    'Model C: Thailand Asymmetry (Nominal ER)': [
        'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_exchange_rate', 
        'covid_dummy', 'post_covid', 'thailand_post_covid'
    ],
    'Model D: Baseline (RER)': [
        'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 'covid_dummy'
    ],
    'Model F: Thailand Asymmetry (RER)': [
        'peace_index', 'ln_cpi', 'ln_gdp_china', 'ln_rer', 
        'covid_dummy', 'post_covid', 'thailand_post_covid'
    ]
}

# ==========================================
# 3. CALCULATE VIF FOR EACH MODEL
# ==========================================
def calculate_vif(data, variables):
    """Calculate VIF for a set of variables"""
    X = data[variables].copy()
    
    # Add constant for VIF calculation
    X_with_const = sm.add_constant(X)
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = variables
    vif_data["VIF"] = [variance_inflation_factor(X_with_const.values, i+1) 
                       for i in range(len(variables))]
    
    return vif_data.sort_values('VIF', ascending=False)

# Import statsmodels for constant
import statsmodels.api as sm

print("=" * 80)
print("VARIANCE INFLATION FACTORS (VIF)")
print("=" * 80)
print("Rule of thumb:")
print("  VIF < 5:  Low multicollinearity (acceptable)")
print("  VIF 5-10: Moderate multicollinearity (caution)")
print("  VIF > 10: High multicollinearity (problematic)")
print()

all_vif_results = {}

for model_name, variables in models.items():
    print(f"\n{model_name}")
    print("-" * 80)
    
    # Calculate VIF
    vif_df = calculate_vif(df, variables)
    all_vif_results[model_name] = vif_df
    
    # Display results
    print(vif_df.to_string(index=False))
    
    # Flag problematic variables
    high_vif = vif_df[vif_df['VIF'] > 10]
    if len(high_vif) > 0:
        print(f"\n⚠️  WARNING: {len(high_vif)} variable(s) with VIF > 10:")
        for _, row in high_vif.iterrows():
            print(f"   - {row['Variable']}: VIF = {row['VIF']:.2f}")
    else:
        print("\n✓ All VIF values < 10 (acceptable)")

# Save VIF results to CSV
vif_output = pd.DataFrame()
for model_name, vif_df in all_vif_results.items():
    vif_df_copy = vif_df.copy()
    vif_df_copy['Model'] = model_name
    vif_output = pd.concat([vif_output, vif_df_copy], ignore_index=True)

vif_output = vif_output[['Model', 'Variable', 'VIF']]
vif_output.to_csv(os.path.join(script_dir, 'vif_results.csv'), index=False)
print(f"\n✓ VIF results saved to: vif_results.csv")

# ==========================================
# 4. CORRELATION MATRICES
# ==========================================
print("\n" + "=" * 80)
print("CORRELATION MATRICES")
print("=" * 80)

# Create correlation matrix for each model's variables
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes = axes.flatten()

for idx, (model_name, variables) in enumerate(models.items()):
    # Calculate correlation matrix
    corr_matrix = df[variables].corr()
    
    # Plot heatmap
    ax = axes[idx]
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={'label': 'Correlation'})
    ax.set_title(f'{model_name}\nCorrelation Matrix', fontsize=12, fontweight='bold')
    
    # Rotate labels for readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    # Print high correlations
    print(f"\n{model_name}")
    print("-" * 80)
    print("High correlations (|r| > 0.7):")
    
    high_corr_found = False
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                var1 = corr_matrix.columns[i]
                var2 = corr_matrix.columns[j]
                print(f"  {var1} ↔ {var2}: r = {corr_val:.3f}")
                high_corr_found = True
    
    if not high_corr_found:
        print("  None (all |r| < 0.7)")

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'correlation_matrices.png'), dpi=300, bbox_inches='tight')
print(f"\n✓ Correlation matrices saved to: correlation_matrices.png")

# ==========================================
# 5. CONDITION NUMBER (OVERALL MULTICOLLINEARITY)
# ==========================================
print("\n" + "=" * 80)
print("CONDITION NUMBERS")
print("=" * 80)
print("Rule of thumb:")
print("  κ < 30:   Low multicollinearity")
print("  κ 30-100: Moderate multicollinearity")
print("  κ > 100:  Severe multicollinearity")
print()

condition_numbers = {}

for model_name, variables in models.items():
    X = df[variables].copy()
    X_standardized = (X - X.mean()) / X.std()
    
    # Calculate condition number
    eigenvalues = np.linalg.eigvals(X_standardized.T @ X_standardized)
    condition_number = np.sqrt(eigenvalues.max() / eigenvalues.min())
    
    condition_numbers[model_name] = condition_number
    
    status = "✓" if condition_number < 30 else "⚠️" if condition_number < 100 else "❌"
    print(f"{status} {model_name}: κ = {condition_number:.2f}")

# ==========================================
# 6. SUMMARY REPORT
# ==========================================
print("\n" + "=" * 80)
print("DIAGNOSTIC SUMMARY")
print("=" * 80)

summary_lines = []
summary_lines.append("=" * 80)
summary_lines.append("MULTICOLLINEARITY DIAGNOSTIC SUMMARY")
summary_lines.append("=" * 80)
summary_lines.append(f"Dataset: {len(df)} observations, {df['Country'].nunique()} countries")
summary_lines.append(f"Years: {df['Year'].min()}-{df['Year'].max()}")
summary_lines.append("")

for model_name, variables in models.items():
    summary_lines.append(f"\n{model_name}")
    summary_lines.append("-" * 80)
    
    # VIF summary
    vif_df = all_vif_results[model_name]
    max_vif = vif_df['VIF'].max()
    high_vif_count = (vif_df['VIF'] > 10).sum()
    
    summary_lines.append(f"VIF Analysis:")
    summary_lines.append(f"  Max VIF: {max_vif:.2f}")
    summary_lines.append(f"  Variables with VIF > 10: {high_vif_count}")
    
    if high_vif_count > 0:
        summary_lines.append(f"  ⚠️  Problematic variables:")
        for _, row in vif_df[vif_df['VIF'] > 10].iterrows():
            summary_lines.append(f"     - {row['Variable']}: {row['VIF']:.2f}")
    
    # Condition number
    kappa = condition_numbers[model_name]
    summary_lines.append(f"\nCondition Number: {kappa:.2f}")
    
    if kappa < 30:
        summary_lines.append("  ✓ Low multicollinearity")
    elif kappa < 100:
        summary_lines.append("  ⚠️  Moderate multicollinearity")
    else:
        summary_lines.append("  ❌ Severe multicollinearity")
    
    # Correlation summary
    corr_matrix = df[variables].corr()
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.7:
                high_corr_pairs.append((corr_matrix.columns[i], 
                                       corr_matrix.columns[j], 
                                       corr_matrix.iloc[i, j]))
    
    summary_lines.append(f"\nHigh Correlations (|r| > 0.7): {len(high_corr_pairs)}")
    for var1, var2, corr_val in high_corr_pairs:
        summary_lines.append(f"  {var1} ↔ {var2}: r = {corr_val:.3f}")

summary_lines.append("\n" + "=" * 80)
summary_lines.append("INTERPRETATION GUIDE")
summary_lines.append("=" * 80)
summary_lines.append("""
VIF (Variance Inflation Factor):
- Measures how much the variance of a coefficient is inflated due to collinearity
- VIF = 1/(1 - R²) where R² is from regressing that variable on all others
- High VIF means the variable is highly predictable from other variables

Condition Number (κ):
- Measures overall multicollinearity in the design matrix
- Based on ratio of largest to smallest eigenvalue
- High κ means the matrix is nearly singular (ill-conditioned)

Correlation:
- Pairwise linear relationships between variables
- High correlation (|r| > 0.7) suggests potential multicollinearity
- But multicollinearity can exist even with low pairwise correlations

Common Issues in Tourism Models:
1. CPI and Exchange Rate: Both measure price/cost effects
2. GDP and Time Trend: Economic growth is time-trending
3. COVID and Post-COVID: Temporal overlap creates collinearity
4. RER and CPI: RER is constructed from exchange rate and CPI ratio
""")

summary_text = "\n".join(summary_lines)
print(summary_text)

# Save summary
with open(os.path.join(script_dir, 'multicollinearity_summary.txt'), 'w') as f:
    f.write(summary_text)

print(f"\n✓ Summary saved to: multicollinearity_summary.txt")

# ==========================================
# 7. CREATE SIMPLE VISUALIZATION FOR DASHBOARD
# ==========================================
# Create a clean VIF comparison chart
fig, ax = plt.subplots(figsize=(12, 8))

# Prepare data for plotting
plot_data = []
for model_name, vif_df in all_vif_results.items():
    for _, row in vif_df.iterrows():
        plot_data.append({
            'Model': model_name.split(':')[0],  # Shorten name
            'Variable': row['Variable'],
            'VIF': row['VIF']
        })

plot_df = pd.DataFrame(plot_data)

# Create grouped bar chart
models_short = plot_df['Model'].unique()
variables = plot_df['Variable'].unique()
x = np.arange(len(variables))
width = 0.2

for i, model in enumerate(models_short):
    model_data = plot_df[plot_df['Model'] == model]
    vif_values = [model_data[model_data['Variable'] == var]['VIF'].values[0] 
                  if var in model_data['Variable'].values else 0 
                  for var in variables]
    ax.bar(x + i*width, vif_values, width, label=model)

ax.set_xlabel('Variable', fontsize=12, fontweight='bold')
ax.set_ylabel('VIF', fontsize=12, fontweight='bold')
ax.set_title('Variance Inflation Factors Across Models', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(variables, rotation=45, ha='right')
ax.axhline(y=5, color='orange', linestyle='--', linewidth=1, label='Moderate (VIF=5)')
ax.axhline(y=10, color='red', linestyle='--', linewidth=1, label='High (VIF=10)')
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'vif_comparison.png'), dpi=300, bbox_inches='tight')
print(f"✓ VIF comparison chart saved to: vif_comparison.png")

print("\n" + "=" * 80)
print("DIAGNOSTICS COMPLETE")
print("=" * 80)
print("Generated files:")
print("  1. vif_results.csv - VIF values for all models")
print("  2. correlation_matrices.png - Correlation heatmaps")
print("  3. vif_comparison.png - VIF comparison chart")
print("  4. multicollinearity_summary.txt - Full diagnostic report")
