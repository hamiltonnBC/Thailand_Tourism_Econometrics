import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'final_regressions/new_models_data')
output_dir = script_dir  # Save results in the main directory

# ==========================================
# MODEL 1: THAILAND TIME SERIES (2000-2024)
# ==========================================
print("=" * 80)
print("RUNNING MODEL 1: THAILAND TIME SERIES (2000-2024)")
print("=" * 80)

# Load data
thailand_ts = pd.read_csv(os.path.join(data_dir, 'thailand_timeseries.csv'))

# Define variables
y = thailand_ts['ln_arrivals']
X = thailand_ts[['ln_gdp_china', 'ln_rer', 'covid_dummy']]
X = sm.add_constant(X)

# Run OLS
model1 = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 1})
print(model1.summary())

# Save results
with open(os.path.join(output_dir, 'model1_thailand_timeseries_results.txt'), 'w') as f:
    f.write(model1.summary().as_text())

# Plot Actual vs Predicted
plt.figure(figsize=(12, 6))
plt.plot(thailand_ts['Year'], thailand_ts['ln_arrivals'], label='Actual Log Arrivals', marker='o', linewidth=2)
plt.plot(thailand_ts['Year'], model1.predict(X), label='Predicted Log Arrivals', linestyle='--', marker='x', linewidth=2)
plt.title('Model 1: Thailand Tourism Demand (Actual vs Predicted)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Log Arrivals')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, 'model1_actual_vs_predicted.png'), dpi=300)
plt.close()

# ==========================================
# MODEL 2: COMPETITOR PANEL (2008-2024)
# ==========================================
print("\n" + "=" * 80)
print("RUNNING MODEL 2: COMPETITOR PANEL (2008-2024)")
print("=" * 80)

# Load data
panel_df = pd.read_csv(os.path.join(data_dir, 'competitor_panel.csv'))
panel_df = panel_df.set_index(['Country', 'Year'])

# Define variables
y_panel = panel_df['ln_arrivals']
exog_vars = ['ln_gdp_china', 'ln_rer', 'peace_index', 'covid_dummy', 'post_covid', 'thailand_post_covid']
X_panel = sm.add_constant(panel_df[exog_vars])

# Run Panel OLS with Entity Effects
model2 = PanelOLS(y_panel, X_panel, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)
print(model2)

# Save results
with open(os.path.join(output_dir, 'model2_competitor_panel_results.txt'), 'w') as f:
    f.write(str(model2))

# ==========================================
# VISUALIZATION: RECOVERY SCORECARD
# ==========================================
print("\nGenerating Recovery Scorecard...")

# Calculate recovery (2024 vs 2019)
recovery_df = pd.read_csv(os.path.join(data_dir, 'competitor_panel.csv'))
recovery_stats = []

for country in recovery_df['Country'].unique():
    try:
        val_2019 = recovery_df[(recovery_df['Country'] == country) & (recovery_df['Year'] == 2019)]['arrivals_from_china'].values[0]
        val_2024 = recovery_df[(recovery_df['Country'] == country) & (recovery_df['Year'] == 2024)]['arrivals_from_china'].values[0]
        recovery_rate = (val_2024 / val_2019) * 100
        recovery_stats.append({'Country': country, 'Recovery_Rate': recovery_rate})
    except IndexError:
        print(f"Skipping {country} due to missing 2019 or 2024 data")

recovery_final = pd.DataFrame(recovery_stats).sort_values('Recovery_Rate', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Recovery_Rate', data=recovery_final, palette='viridis')
plt.axhline(y=100, color='r', linestyle='--', label='Pre-COVID Level (100%)')
plt.title('Tourism Recovery Scorecard: 2024 Arrivals vs 2019', fontsize=14)
plt.ylabel('Recovery Rate (%)')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.savefig(os.path.join(output_dir, 'recovery_scorecard.png'), dpi=300)
plt.close()

print("\nAnalysis Complete. Files generated:")
print(f"1. {os.path.join(output_dir, 'model1_thailand_timeseries_results.txt')}")
print(f"2. {os.path.join(output_dir, 'model1_actual_vs_predicted.png')}")
print(f"3. {os.path.join(output_dir, 'model2_competitor_panel_results.txt')}")
print(f"4. {os.path.join(output_dir, 'recovery_scorecard.png')}")
