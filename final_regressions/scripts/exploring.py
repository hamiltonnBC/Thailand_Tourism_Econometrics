import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('../Primary_Dataset_For_Panel_FINAL.csv')

print("=" * 80)
print("DATASET ANALYSIS: Primary_Dataset_For_Panel_FINAL.csv")
print("=" * 80)

# Basic dataset information
print("\n1. DATASET OVERVIEW")
print("-" * 80)
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Columns: {', '.join(df.columns.tolist())}")

# List all unique countries
print("\n2. COUNTRIES IN DATASET")
print("-" * 80)
countries = sorted(df['Country'].unique())
print(f"Total countries: {len(countries)}")
for i, country in enumerate(countries, 1):
    print(f"{i:2d}. {country}")

# Year range
print("\n3. YEAR RANGE")
print("-" * 80)
print(f"Years covered: {df['Year'].min()} - {df['Year'].max()}")
print(f"Total years: {df['Year'].nunique()}")

# Overall missing data summary
print("\n4. OVERALL MISSING DATA SUMMARY")
print("-" * 80)
missing_summary = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing_summary,
    'Missing %': missing_pct
}).sort_values('Missing Count', ascending=False)
print(missing_df)

# Missing data by column
print("\n5. DETAILED MISSING DATA BY COLUMN")
print("-" * 80)
for col in df.columns:
    if col not in ['Country', 'Year']:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            print(f"\n{col}:")
            print(f"  Total missing: {missing_count} ({(missing_count/len(df)*100):.2f}%)")
            
            # Countries with missing data for this column
            missing_countries = df[df[col].isnull()]['Country'].unique()
            print(f"  Countries with missing data: {len(missing_countries)}")
            for country in sorted(missing_countries):
                country_missing = df[(df['Country'] == country) & (df[col].isnull())]
                years = sorted(country_missing['Year'].tolist())
                print(f"    - {country}: {len(years)} years missing - {years}")

# Missing data by country
print("\n6. MISSING DATA BY COUNTRY")
print("-" * 80)
for country in countries:
    country_df = df[df['Country'] == country]
    print(f"\n{country}:")
    print(f"  Total records: {len(country_df)}")
    print(f"  Year range: {country_df['Year'].min()} - {country_df['Year'].max()}")
    
    # Check each column for missing data
    has_missing = False
    for col in df.columns:
        if col not in ['Country', 'Year']:
            missing_count = country_df[col].isnull().sum()
            if missing_count > 0:
                has_missing = True
                missing_years = sorted(country_df[country_df[col].isnull()]['Year'].tolist())
                print(f"    {col}: {missing_count}/{len(country_df)} missing ({(missing_count/len(country_df)*100):.2f}%)")
                print(f"      Years: {missing_years}")
    
    if not has_missing:
        print("    No missing data!")

# Data completeness by year
print("\n7. DATA COMPLETENESS BY YEAR")
print("-" * 80)
years = sorted(df['Year'].unique())
for year in years:
    year_df = df[df['Year'] == year]
    total_cells = len(year_df) * (len(df.columns) - 2)  # Exclude Country and Year
    missing_cells = year_df.drop(['Country', 'Year'], axis=1).isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    print(f"  {year}: {len(year_df)} countries, {completeness:.2f}% complete, {missing_cells} missing values")

# Countries with complete data
print("\n8. COUNTRIES WITH COMPLETE DATA (NO MISSING VALUES)")
print("-" * 80)
complete_countries = []
for country in countries:
    country_df = df[df['Country'] == country]
    if country_df.drop(['Country', 'Year'], axis=1).isnull().sum().sum() == 0:
        complete_countries.append(country)

if complete_countries:
    for country in complete_countries:
        print(f"  - {country}")
else:
    print("  No countries with complete data across all years and columns")

# Most complete countries
print("\n9. COUNTRIES RANKED BY DATA COMPLETENESS")
print("-" * 80)
country_completeness = []
for country in countries:
    country_df = df[df['Country'] == country]
    total_cells = len(country_df) * (len(df.columns) - 2)
    missing_cells = country_df.drop(['Country', 'Year'], axis=1).isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    country_completeness.append((country, completeness, missing_cells, total_cells))

country_completeness.sort(key=lambda x: x[1], reverse=True)
for country, completeness, missing, total in country_completeness:
    print(f"  {country}: {completeness:.2f}% complete ({missing}/{total} missing)")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
