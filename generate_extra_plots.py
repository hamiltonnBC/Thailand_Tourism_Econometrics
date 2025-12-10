import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'final_regressions/new_models_data')
output_dir = script_dir

# Load Thailand Data
df = pd.read_csv(os.path.join(data_dir, 'thailand_timeseries.csv'))

# 1. Correlation Heatmap
plt.figure(figsize=(10, 8))
corr_vars = ['ln_arrivals', 'ln_gdp_china', 'ln_rer', 'ln_cpi', 'covid_dummy']
labels = ['Log Arrivals', 'Log GDP (China)', 'Log RER', 'Log CPI (Thai)', 'COVID Dummy']
corr = df[corr_vars].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, xticklabels=labels, yticklabels=labels)
plt.title('Correlation Matrix: Thailand Tourism Variables (2000-2024)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'thailand_correlation_matrix.png'), dpi=300)
plt.close()

# 2. Key Trends (Dual Axis)
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('Log Chinese Arrivals', color=color)
ax1.plot(df['Year'], df['ln_arrivals'], color=color, linewidth=3, label='Log Arrivals')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Log GDP China', color=color)  # we already handled the x-label with ax1
ax2.plot(df['Year'], df['ln_gdp_china'], color=color, linewidth=3, linestyle='--', label='Log GDP China')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Drivers of Tourism: Arrivals vs Chinese GDP (2000-2024)', fontsize=14)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig(os.path.join(output_dir, 'thailand_trends_gdp.png'), dpi=300)
plt.close()

# 3. RER Trend
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['RER'], color='green', linewidth=2, marker='o')
plt.axhline(y=df['RER'].mean(), color='gray', linestyle='--', label='Mean RER')
plt.title('Real Exchange Rate (RER) Fluctuations: Thailand (2000-2024)', fontsize=14)
plt.ylabel('RER Index (Higher = More Expensive for Chinese)', fontsize=12)
plt.xlabel('Year')
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig(os.path.join(output_dir, 'thailand_rer_trend.png'), dpi=300)
plt.close()

print("Generated 3 additional plots.")
