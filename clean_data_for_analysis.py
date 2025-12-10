import pandas as pd
import numpy as np
import os

# Set paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'final_regressions/Primary_Dataset_For_Panel_FINAL.csv')
output_dir = os.path.join(script_dir, 'final_regressions/new_models_data')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load data
print(f"Loading data from {data_path}...")
df = pd.read_csv(data_path)

# ==========================================
# 1. PREPARE THAILAND TIME SERIES (2000-2024)
# ==========================================
print("\nProcessing Thailand Time Series (2000-2024)...")
thailand_df = df[df['Country'] == 'Thailand'].copy()

# Filter years 2000-2024
thailand_df = thailand_df[(thailand_df['Year'] >= 2000) & (thailand_df['Year'] <= 2024)]

# Select columns
ts_cols = ['Year', 'arrivals_from_china', 'gdp_china', 'exchange_rate', 'RER', 'CPI_destination']
thailand_ts = thailand_df[ts_cols].copy()

# Create dummy variables
thailand_ts['covid_dummy'] = ((thailand_ts['Year'] >= 2020) & (thailand_ts['Year'] <= 2022)).astype(int)
thailand_ts['post_covid'] = (thailand_ts['Year'] >= 2023).astype(int)

# Log transform key variables
thailand_ts['ln_arrivals'] = np.log(thailand_ts['arrivals_from_china'])
thailand_ts['ln_gdp_china'] = np.log(thailand_ts['gdp_china'])
thailand_ts['ln_rer'] = np.log(thailand_ts['RER'])
thailand_ts['ln_cpi'] = np.log(thailand_ts['CPI_destination'])

# Save to CSV
ts_output_path = os.path.join(output_dir, 'thailand_timeseries.csv')
thailand_ts.to_csv(ts_output_path, index=False)
print(f"✓ Saved {len(thailand_ts)} observations to {ts_output_path}")

# ==========================================
# 2. PREPARE COMPETITOR PANEL (2008-2024)
# ==========================================
print("\nProcessing Competitor Panel (2008-2024)...")
competitors = ['Thailand', 'Viet Nam', 'Malaysia', 'Indonesia']
panel_df = df[df['Country'].isin(competitors)].copy()

# Filter years 2008-2024 (constrained by peace_index availability if we wanted it, but good for stability)
panel_df = panel_df[(panel_df['Year'] >= 2008) & (panel_df['Year'] <= 2024)]

# Select columns
panel_cols = ['Country', 'Year', 'arrivals_from_china', 'gdp_china', 'exchange_rate', 'RER', 'peace_index', 'CPI_destination']
panel_clean = panel_df[panel_cols].copy()

# Handle missing values
# Check for missing values
print("Missing values before cleaning:")
print(panel_clean.isnull().sum())

# Drop rows with missing arrivals or RER
panel_clean = panel_clean.dropna(subset=['arrivals_from_china', 'RER'])

# Create dummy variables
panel_clean['covid_dummy'] = ((panel_clean['Year'] >= 2020) & (panel_clean['Year'] <= 2022)).astype(int)
panel_clean['post_covid'] = (panel_clean['Year'] >= 2023).astype(int)
panel_clean['is_thailand'] = (panel_clean['Country'] == 'Thailand').astype(int)
panel_clean['thailand_post_covid'] = panel_clean['is_thailand'] * panel_clean['post_covid']

# Log transform
panel_clean['ln_arrivals'] = np.log(panel_clean['arrivals_from_china'])
panel_clean['ln_gdp_china'] = np.log(panel_clean['gdp_china'])
panel_clean['ln_rer'] = np.log(panel_clean['RER'])

# Save to CSV
panel_output_path = os.path.join(output_dir, 'competitor_panel.csv')
panel_clean.to_csv(panel_output_path, index=False)
print(f"✓ Saved {len(panel_clean)} observations to {panel_output_path}")
print(f"   Countries included: {panel_clean['Country'].unique()}")

print("\nData preparation complete.")
