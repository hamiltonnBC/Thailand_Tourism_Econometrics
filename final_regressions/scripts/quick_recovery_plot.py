import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../Primary_Dataset_For_Panel_FINAL.csv')

# Filter for 2019-2024 and remove missing data
df = df[(df['Year'] >= 2019) & (df['Year'] <= 2024)]
df = df.dropna(subset=['arrivals_from_china'])

# Create plot
plt.figure(figsize=(14, 8))

for country in sorted(df['Country'].unique()):
    data = df[df['Country'] == country]
    plt.plot(data['Year'], data['arrivals_from_china'], 
             marker='o', linewidth=2.5, markersize=8, label=country)

plt.axvline(x=2020, color='red', linestyle='--', linewidth=2, alpha=0.6)
plt.axvline(x=2022, color='green', linestyle='--', linewidth=2, alpha=0.6)

plt.xlabel('Year', fontsize=14)
plt.ylabel('Chinese Tourist Arrivals', fontsize=14)
plt.title('Chinese Tourist Arrivals by Country (2019-2024)', fontsize=16)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig('recovery_comparison_2019_2024.png', dpi=300, bbox_inches='tight')
print("✓ Saved: recovery_comparison_2019_2024.png")
plt.show()
