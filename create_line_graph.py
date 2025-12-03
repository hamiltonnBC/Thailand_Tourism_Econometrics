import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('data/Countries_Compared.csv')

# Select only the year columns from 2012 to 2022
year_columns = [str(year) for year in range(2012, 2023)]
countries = df['Country'].tolist()

# Create the figure and axis
plt.figure(figsize=(14, 8))

# Plot each country
for idx, country in enumerate(countries):
    # Get the data for this country
    values = []
    for year in year_columns:
        val = df.loc[df['Country'] == country, year].values[0]
        # Handle missing values and remove commas
        if pd.isna(val) or val == '':
            values.append(np.nan)
        else:
            # Remove commas and convert to float
            values.append(float(str(val).replace(',', '')))
    
    # Plot the line
    plt.plot(year_columns, values, marker='o', linewidth=2, label=country, markersize=5)

# Customize the plot
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Number of Visitors', fontsize=12, fontweight='bold')
plt.title('Tourism Data by Country (2012-2022)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Format y-axis to show numbers in millions
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

# Save the plot
plt.savefig('tourism_line_graph_2012_2022.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'tourism_line_graph_2012_2022.png'")

# Show the plot
plt.show()
