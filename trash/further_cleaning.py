import pandas as pd
import numpy as np

# Read the reformatted CSV file
csv_file = '../data/API_Data/P_Data_Extract_From_World_Development_Indicators/filtered_reformatted.csv'
df = pd.read_csv(csv_file)

print("=" * 80)
print("DATA QUALITY ANALYSIS FOR ECONOMETRICS PROJECT")
print("=" * 80)

# Basic info
print("\n1. DATASET OVERVIEW")
print("-" * 80)
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")

# Check for null values
print("\n2. NULL/MISSING VALUES")
print("-" * 80)
null_counts = df.isnull().sum()
print(f"Null values per column:\n{null_counts}")
print(f"\nTotal null values: {df.isnull().sum().sum()}")

# Check for empty strings or whitespace
print("\n3. EMPTY OR WHITESPACE VALUES")
print("-" * 80)
for col in df.columns:
    if df[col].dtype == 'object':
        empty_count = (df[col].str.strip() == '').sum()
        if empty_count > 0:
            print(f"{col}: {empty_count} empty/whitespace values")

# Year range analysis
print("\n4. YEAR COVERAGE")
print("-" * 80)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
print(f"Year range: {df['Year'].min()} to {df['Year'].max()}")
print(f"Unique years: {sorted(df['Year'].unique())}")
print(f"Total unique years: {df['Year'].nunique()}")

# Check for missing years by country and series
print("\n5. MISSING YEARS BY COUNTRY AND SERIES")
print("-" * 80)
all_years = set(range(int(df['Year'].min()), int(df['Year'].max()) + 1))

for country in df['Country Name'].unique():
    print(f"\n{country}:")
    for series in df['Series Name'].unique():
        subset = df[(df['Country Name'] == country) & (df['Series Name'] == series)]
        available_years = set(subset['Year'].values)
        missing_years = sorted(all_years - available_years)
        
        if missing_years:
            print(f"  {series}:")
            print(f"    Available: {len(available_years)} years")
            print(f"    Missing: {len(missing_years)} years - {missing_years}")
        else:
            print(f"  {series}: Complete (all years present)")

# Value analysis
print("\n6. VALUE COLUMN ANALYSIS")
print("-" * 80)
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
print(f"Value statistics:\n{df['Value'].describe()}")
print(f"\nNull values in Value column: {df['Value'].isnull().sum()}")
print(f"Zero values: {(df['Value'] == 0).sum()}")
print(f"Negative values: {(df['Value'] < 0).sum()}")

# Check for duplicates
print("\n7. DUPLICATE ROWS")
print("-" * 80)
duplicates = df.duplicated(subset=['Country Name', 'Series Code', 'Year'])
print(f"Duplicate rows: {duplicates.sum()}")
if duplicates.sum() > 0:
    print("\nDuplicate entries:")
    print(df[duplicates])

# Data completeness by series
print("\n8. DATA COMPLETENESS BY SERIES")
print("-" * 80)
for series in df['Series Name'].unique():
    series_data = df[df['Series Name'] == series]
    total_possible = len(df['Country Name'].unique()) * df['Year'].nunique()
    actual_count = len(series_data)
    completeness = (actual_count / total_possible) * 100
    print(f"{series}:")
    print(f"  Rows: {actual_count} / {total_possible} ({completeness:.1f}% complete)")

# Check for outliers (using IQR method)
print("\n9. POTENTIAL OUTLIERS (IQR METHOD)")
print("-" * 80)
for series in df['Series Name'].unique():
    series_data = df[df['Series Name'] == series]['Value'].dropna()
    if len(series_data) > 0:
        Q1 = series_data.quantile(0.25)
        Q3 = series_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = series_data[(series_data < lower_bound) | (series_data > upper_bound)]
        if len(outliers) > 0:
            print(f"{series}: {len(outliers)} potential outliers")

# Summary and recommendations
print("\n10. RECOMMENDATIONS FOR ECONOMETRICS")
print("=" * 80)
print("✓ Check if missing years need interpolation or should be excluded")
print("✓ Verify if negative values (e.g., negative GDP growth) are expected")
print("✓ Consider handling missing data with:")
print("  - Forward/backward fill for time series continuity")
print("  - Interpolation for missing years")
print("  - Exclusion of incomplete series if necessary")
print("✓ Ensure all series have matching time periods for regression analysis")
print("✓ Check for stationarity in time series data before modeling")
print("✓ Consider logging GDP values to handle scale differences")
print("=" * 80)
