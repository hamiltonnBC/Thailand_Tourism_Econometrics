import pandas as pd
import numpy as np

# Read the primary dataset (with fixed CPI)
df_primary = pd.read_csv('Primary_Dataset_For_Panel.xlsx - Sheet1_fixed_CPI.csv')

# Read the peace index data
df_peace = pd.read_csv('GlobalPeaceIndexData.csv')

# Clean up the country column name (has trailing space)
df_peace.columns = [col.strip() for col in df_peace.columns]

# Melt the peace index data from wide to long format
# This converts year columns into rows
df_peace_long = df_peace.melt(
    id_vars=['Country'],
    var_name='Year',
    value_name='peace_index_new'
)

# Convert Year to integer
df_peace_long['Year'] = df_peace_long['Year'].astype(int)

# Merge with primary dataset
# First, drop the old peace_index column if it exists
if 'peace_index' in df_primary.columns:
    df_primary = df_primary.drop('peace_index', axis=1)

# Merge on Country and Year
df_merged = df_primary.merge(
    df_peace_long,
    on=['Country', 'Year'],
    how='left'
)

# Rename the new peace index column to peace_index
df_merged = df_merged.rename(columns={'peace_index_new': 'peace_index'})

# Reorder columns to put peace_index in a logical position
# (after visa_free, before cpi)
cols = df_merged.columns.tolist()
if 'peace_index' in cols:
    cols.remove('peace_index')
    # Find position to insert (after visa_free)
    if 'visa_free' in cols:
        insert_pos = cols.index('visa_free') + 1
    else:
        insert_pos = 5  # default position
    cols.insert(insert_pos, 'peace_index')
    df_merged = df_merged[cols]

# Save to new CSV
output_filename = 'Primary_Dataset_For_Panel.xlsx - Sheet1_fixed_CPI_with_peace.csv'
df_merged.to_csv(output_filename, index=False)

print(f"✓ Peace index data merged successfully!")
print(f"✓ Saved to: {output_filename}")
print(f"\nSample data for Thailand (2020-2024):")
thailand_sample = df_merged[
    (df_merged['Country'] == 'Thailand') & 
    (df_merged['Year'] >= 2020)
][['Country', 'Year', 'peace_index', 'cpi', 'cpi_index']]
print(thailand_sample.to_string(index=False))

print(f"\nPeace index coverage:")
print(f"Total rows: {len(df_merged)}")
print(f"Rows with peace index: {df_merged['peace_index'].notna().sum()}")
print(f"Rows missing peace index: {df_merged['peace_index'].isna().sum()}")
