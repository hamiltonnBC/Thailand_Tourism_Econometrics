import pandas as pd
import numpy as np

# Read the current dataset (with peace index)
df_primary = pd.read_csv('Primary_Dataset_For_Panel.xlsx - Sheet1_fixed_CPI_with_peace.csv')

# Read the correct CPI index data
df_cpi = pd.read_csv('CPI_INDEX_CORRECT.csv')

# Melt the CPI index data from wide to long format
df_cpi_long = df_cpi.melt(
    id_vars=['Country'],
    var_name='Year',
    value_name='cpi_index_correct'
)

# Convert Year to integer
df_cpi_long['Year'] = df_cpi_long['Year'].astype(int)

# Drop the old cpi_index column
if 'cpi_index' in df_primary.columns:
    df_primary = df_primary.drop('cpi_index', axis=1)

# Merge with primary dataset
df_merged = df_primary.merge(
    df_cpi_long,
    on=['Country', 'Year'],
    how='left'
)

# Rename the new CPI index column to cpi_index
df_merged = df_merged.rename(columns={'cpi_index_correct': 'cpi_index'})

# Reorder columns to put cpi_index after cpi
cols = df_merged.columns.tolist()
if 'cpi_index' in cols and 'cpi' in cols:
    cols.remove('cpi_index')
    cpi_pos = cols.index('cpi')
    cols.insert(cpi_pos + 1, 'cpi_index')
    df_merged = df_merged[cols]

# Save to new CSV
output_filename = 'Primary_Dataset_For_Panel_FINAL.csv'
df_merged.to_csv(output_filename, index=False)

print(f"✓ CPI index updated successfully!")
print(f"✓ Saved to: {output_filename}")
print(f"\nSample data for Thailand (2020-2024):")
thailand_sample = df_merged[
    (df_merged['Country'] == 'Thailand') & 
    (df_merged['Year'] >= 2020)
][['Country', 'Year', 'peace_index', 'cpi', 'cpi_index']]
print(thailand_sample.to_string(index=False))

print(f"\nSample data for Australia (2008-2012):")
australia_sample = df_merged[
    (df_merged['Country'] == 'Australia') & 
    (df_merged['Year'] >= 2008) & 
    (df_merged['Year'] <= 2012)
][['Country', 'Year', 'peace_index', 'cpi', 'cpi_index']]
print(australia_sample.to_string(index=False))

print(f"\nData coverage:")
print(f"Total rows: {len(df_merged)}")
print(f"Rows with CPI index: {df_merged['cpi_index'].notna().sum()}")
print(f"Rows with peace index: {df_merged['peace_index'].notna().sum()}")
