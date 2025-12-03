import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('final_regressions/Primary_Dataset_For_Panel_FINAL.csv')

# Filter for years 2019-2024
df_filtered = df[(df['Year'] >= 2019) & (df['Year'] <= 2024)]

# Get unique countries
countries = df_filtered['Country'].unique()

# Create the plot
plt.figure(figsize=(14, 8))

for country in countries:
    country_data = df_filtered[df_filtered['Country'] == country].sort_values('Year')
    plt.plot(country_data['Year'], country_data['arrivals_from_china'], 
             marker='o', label=country, linewidth=2)

plt.xlabel('Year', fontsize=12)
plt.ylabel('Arrivals from China', fontsize=12)
plt.title('Tourist Arrivals from China by Country (2019-2024)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.xticks([2019, 2020, 2021, 2022, 2023, 2024])
plt.tight_layout()

# Save the plot
plt.savefig('final_regressions/china_arrivals_2019_2024.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'final_regressions/china_arrivals_2019_2024.png'")

plt.show()
