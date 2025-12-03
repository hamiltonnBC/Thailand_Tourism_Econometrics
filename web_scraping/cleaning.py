import pandas as pd
import glob
import os

print("Starting data cleaning and combination process...")

# Get all the xlsx files in the web_scraping directory
file_pattern = "web_scraping/us_news_countries_data_*.xlsx"
files = glob.glob(file_pattern)

print(f"Found {len(files)} files to process\n")

# Initialize the combined dataframe with None
combined_df = None

# Process each file
for file_path in sorted(files):
    # Extract the category name from the filename
    filename = os.path.basename(file_path)
    # Remove 'us_news_countries_data_' prefix and '.xlsx' suffix
    category = filename.replace('us_news_countries_data_', '').replace('.xlsx', '')
    
    print(f"Processing: {filename}")
    print(f"  Category: {category}")
    
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Keep only Country and Rank_Number columns
    if 'Country' in df.columns and 'Rank_Number' in df.columns:
        df_subset = df[['Country', 'Rank_Number']].copy()
        
        # Remove rows where Country is blank/null
        df_subset = df_subset[df_subset['Country'].notna() & (df_subset['Country'] != '')]
        
        # Rename Rank_Number to include the category
        new_column_name = f'Rank_Number_{category}'
        df_subset.rename(columns={'Rank_Number': new_column_name}, inplace=True)
        
        print(f"  Found {len(df_subset)} countries")
        print(f"  Column renamed to: {new_column_name}")
        
        # Merge with combined dataframe
        if combined_df is None:
            combined_df = df_subset
        else:
            combined_df = pd.merge(combined_df, df_subset, on='Country', how='outer')
        
        print(f"  Combined dataframe now has {len(combined_df)} rows\n")
    else:
        print(f"  WARNING: Missing required columns in {filename}\n")

# Remove any rows where Country is blank
combined_df = combined_df[combined_df['Country'].notna() & (combined_df['Country'] != '')]

# Sort by Country name
combined_df = combined_df.sort_values('Country').reset_index(drop=True)

# Save to Excel
output_file = 'web_scraping/us_news_countries_combined.xlsx'
print(f"Saving combined data to: {output_file}")
combined_df.to_excel(output_file, index=False, engine='openpyxl')

print(f"\n✓ Successfully combined {len(files)} files")
print(f"✓ Total countries: {len(combined_df)}")
print(f"✓ Total columns: {len(combined_df.columns)}")
print(f"✓ Output saved to: {output_file}")

print("\nColumn names:")
for col in combined_df.columns:
    print(f"  - {col}")

print("\nFirst few rows:")
print(combined_df.head(10))

print("\nData summary:")
print(combined_df.info())
