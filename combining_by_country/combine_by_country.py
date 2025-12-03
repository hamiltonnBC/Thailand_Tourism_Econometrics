import pandas as pd
import os

# Country name standardization mapping
country_mapping = {
    'USA': 'United States',
    'UK': 'United Kingdom',
    'United Kingdom (UK)': 'United Kingdom',
    'UAE': 'United Arab Emirates',
    'Russia': 'Russian Federation',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Brunei': 'Brunei Darussalam',
    'Cape Verde': 'Cabo Verde',
    'Congo (Democratic Republic of the)': 'Democratic Republic of the Congo (DRC)',
    'Czechia': 'Czech Republic',
    'Cote d\'Ivoire': 'Côte d\'Ivoire',
    'Eswatini': 'Eswatini (Kingdom of)',
    'Hong Kong': 'Hong Kong, China (SAR)',
    'Iran': 'Iran (Islamic Republic of)',
    'Korea (Republic of)': 'South Korea',
    'Korea (Democratic People\'s Rep. of)': 'North Korea',
    'Laos': 'Lao People\'s Democratic Republic',
    'Micronesia': 'Micronesia (Federated States of)',
    'Moldova': 'Moldova (Republic of)',
    'Palestine': 'Palestine, State of',
    'Palestinian territories': 'Palestine, State of',
    'Syria': 'Syrian Arab Republic',
    'Tanzania': 'Tanzania (United Republic of)',
    'Turkey': 'Türkiye',
    'Venezuela': 'Venezuela (Bolivarian Republic of)',
    'Vietnam': 'Viet Nam',
}

def standardize_country_name(name):
    """Standardize country names using the mapping."""
    if pd.isna(name):
        return name
    return country_mapping.get(name, name)

# Input file path
input_file = 'combining_by_country/Econometrics_country_comparison_data_compilation.xlsx'

# Read all sheets from the Excel file
excel_file = pd.ExcelFile(input_file)
sheet_names = excel_file.sheet_names

print(f"Found {len(sheet_names)} sheets: {sheet_names}")


# Initializing the master dataframe with the first sheet
master_df = pd.read_excel(input_file, sheet_name=sheet_names[0])
master_df['Country'] = master_df['Country'].apply(standardize_country_name)
print(f"\nSheet 1 '{sheet_names[0]}': {len(master_df)} countries, {len(master_df.columns)} columns")

# Merge each subsequent sheet using 'Country' as the key
for sheet_name in sheet_names[1:]:
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    df['Country'] = df['Country'].apply(standardize_country_name)
    print(f"Sheet '{sheet_name}': {len(df)} countries, {len(df.columns)} columns")
    
    # Merge on 'Country' column, keeping all countries from both dataframes
    master_df = master_df.merge(df, on='Country', how='outer')
    print(f"  After merge: {len(master_df)} total countries, {len(master_df.columns)} columns")

# Sort by Country name for cleaner output
master_df = master_df.sort_values('Country').reset_index(drop=True)

# Create output filename
output_file = input_file.replace('.xlsx', '_combined.xlsx')

# Save to new Excel file
master_df.to_excel(output_file, index=False)

print(f"\n✓ Combined data saved to: {output_file}")
print(f"Final result: {len(master_df)} countries, {len(master_df.columns)} columns")
