import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Primary_Dataset_For_Panel.xlsx - Sheet1.csv')

# Create a new column for the CPI index
df['cpi_index'] = np.nan

# Process each country separately
for country in df['Country'].unique():
    # Get data for this country
    country_mask = df['Country'] == country
    country_data = df[country_mask].copy()
    
    # Sort by year to ensure proper ordering
    country_data = country_data.sort_values('Year')
    
    # Find the 2010 row for this country
    base_year_mask = (country_data['Year'] == 2010)
    
    if base_year_mask.any():
        # Set 2010 = 100
        base_idx = country_data[base_year_mask].index[0]
        df.loc[base_idx, 'cpi_index'] = 100.0
        
        # Get sorted indices for this country
        sorted_indices = country_data.index.tolist()
        base_position = sorted_indices.index(base_idx)
        
        # Calculate forward (2011, 2012, ...)
        for i in range(base_position + 1, len(sorted_indices)):
            current_idx = sorted_indices[i]
            previous_idx = sorted_indices[i - 1]
            
            inflation_rate = df.loc[current_idx, 'cpi']
            
            if pd.notna(inflation_rate) and pd.notna(df.loc[previous_idx, 'cpi_index']):
                # CPI_current = CPI_previous × (1 + inflation_rate/100)
                df.loc[current_idx, 'cpi_index'] = df.loc[previous_idx, 'cpi_index'] * (1 + inflation_rate / 100)
        
        # Calculate backward (2009, 2008, ...)
        for i in range(base_position - 1, -1, -1):
            current_idx = sorted_indices[i]
            next_idx = sorted_indices[i + 1]
            
            # The inflation rate at next_idx tells us how to get from current to next
            inflation_rate = df.loc[next_idx, 'cpi']
            
            if pd.notna(inflation_rate) and pd.notna(df.loc[next_idx, 'cpi_index']):
                # CPI_previous = CPI_current / (1 + inflation_rate/100)
                df.loc[current_idx, 'cpi_index'] = df.loc[next_idx, 'cpi_index'] / (1 + inflation_rate / 100)

# Save to new CSV file
output_filename = 'cambodia.csv'
df.to_csv(output_filename, index=False)

print(f"✓ CPI index calculated and saved to: {output_filename}")

