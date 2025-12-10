import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('final_regressions/Primary_Dataset_For_Panel_FINAL.csv')

# Filter for Thailand
thailand = df[df['Country'] == 'Thailand'].copy()

# Select relevant columns
cols = ['Year', 'arrivals_from_china', 'CPI_destination', 'gdp_china', 'exchange_rate', 'RER']
thailand = thailand[cols]

# Drop rows with missing values to see what's left
thailand_clean = thailand.dropna()

print("Thailand Data (Cleaned):")
print(thailand_clean.head())
print(f"\nObservations: {len(thailand_clean)}")
print(f"Years: {thailand_clean['Year'].min()} - {thailand_clean['Year'].max()}")

# Correlation matrix
print("\nCorrelation Matrix:")
print(thailand_clean.corr())
