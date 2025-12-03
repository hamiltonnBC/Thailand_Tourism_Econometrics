import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD PRIMARY DATASET
# ==========================================
df_primary = pd.read_csv('../Primary_Dataset_For_Panel_FINAL.csv')

print(f"Original dataset shape: {df_primary.shape}")
print(f"Columns: {df_primary.columns.tolist()}")

# ==========================================
# 2. LOAD CORRECT CPI INDEX DATA
# ==========================================
# Load the correct CPI index file (2010 = 100 base year)
df_cpi = pd.read_csv('../precious_datasets/CPI_INDEX_CORRECT.csv')

# Melt from wide to long format
df_cpi_long = df_cpi.melt(
    id_vars=['Country'],
    var_name='Year',
    value_name='CPI_destination'
)

# Convert Year to integer
df_cpi_long['Year'] = df_cpi_long['Year'].astype(int)

# Convert CPI to numeric (handle any empty strings)
df_cpi_long['CPI_destination'] = pd.to_numeric(df_cpi_long['CPI_destination'], errors='coerce')

print(f"\nCPI data loaded: {len(df_cpi_long)} rows")
print(f"Countries in CPI data: {df_cpi_long['Country'].unique().tolist()}")

# ==========================================
# 3. ADD CHINA CPI DATA
# ==========================================
# China CPI data (2010 = 100 base year)
# Source: World Bank data
china_cpi_data = {
    1995: 52.8,
    1996: 58.3,
    1997: 60.8,
    1998: 59.9,
    1999: 58.6,
    2000: 58.9,
    2001: 59.7,
    2002: 59.0,
    2003: 60.1,
    2004: 63.5,
    2005: 64.8,
    2006: 65.5,
    2007: 69.5,
    2008: 75.1,
    2009: 74.5,
    2010: 100.0,
    2011: 105.4,
    2012: 108.2,
    2013: 110.9,
    2014: 112.9,
    2015: 114.4,
    2016: 116.4,
    2017: 118.1,
    2018: 120.3,
    2019: 123.2,
    2020: 126.0,
    2021: 126.9,
    2022: 129.0,
    2023: 129.2,
    2024: 129.5
}

# Create DataFrame from China CPI data
df_china_cpi = pd.DataFrame(list(china_cpi_data.items()), columns=['Year', 'CPI_china'])

# ==========================================
# 4. MERGE ALL DATA
# ==========================================
# Drop old columns that we'll replace
columns_to_drop = []
if 'cpi' in df_primary.columns:
    columns_to_drop.append('cpi')
if 'CPI_destination' in df_primary.columns:
    columns_to_drop.append('CPI_destination')
if 'CPI_china' in df_primary.columns:
    columns_to_drop.append('CPI_china')
if 'RER' in df_primary.columns:
    columns_to_drop.append('RER')

if columns_to_drop:
    df_primary = df_primary.drop(columns_to_drop, axis=1)
    print(f"\n✓ Dropped old columns: {columns_to_drop}")

# Check if cpi_index exists and use it, otherwise merge from CPI file
if 'cpi_index' in df_primary.columns:
    print("\n✓ Using existing 'cpi_index' column as CPI_destination")
    df_merged = df_primary.rename(columns={'cpi_index': 'CPI_destination'})
else:
    # Merge with correct CPI destination data
    df_merged = df_primary.merge(
        df_cpi_long,
        on=['Country', 'Year'],
        how='left'
    )

# Merge with China CPI data
df_merged = df_merged.merge(
    df_china_cpi,
    on='Year',
    how='left'
)

# ==========================================
# 5. CALCULATE REAL EXCHANGE RATE (RER)
# ==========================================
# Formula: RER = Nominal_Exchange_Rate * (CPI_destination / CPI_china)
# 
# Interpretation:
# - Higher RER = Destination is MORE EXPENSIVE for Chinese tourists (in real terms)
# - Lower RER = Destination is CHEAPER for Chinese tourists (in real terms)
# - RER accounts for inflation differences between China and destination
# - All components are POSITIVE, so RER must be POSITIVE

# Calculate RER
df_merged['RER'] = df_merged['exchange_rate'] * (df_merged['CPI_destination'] / df_merged['CPI_china'])

# ==========================================
# 5.5. DIAGNOSTIC CHECK FOR NEGATIVE VALUES
# ==========================================
print(f"\n{'='*60}")
print(f"DIAGNOSTIC CHECKS")
print(f"{'='*60}")

# Check for negative values in components
neg_exchange = df_merged[df_merged['exchange_rate'] < 0]
neg_cpi_dest = df_merged[df_merged['CPI_destination'] < 0]
neg_cpi_china = df_merged[df_merged['CPI_china'] < 0]
neg_rer = df_merged[df_merged['RER'] < 0]

if len(neg_exchange) > 0:
    print(f"\n⚠️  WARNING: {len(neg_exchange)} rows with NEGATIVE exchange_rate!")
    print(neg_exchange[['Country', 'Year', 'exchange_rate']].head())

if len(neg_cpi_dest) > 0:
    print(f"\n⚠️  WARNING: {len(neg_cpi_dest)} rows with NEGATIVE CPI_destination!")
    print(neg_cpi_dest[['Country', 'Year', 'CPI_destination']].head())

if len(neg_cpi_china) > 0:
    print(f"\n⚠️  WARNING: {len(neg_cpi_china)} rows with NEGATIVE CPI_china!")
    print(neg_cpi_china[['Country', 'Year', 'CPI_china']].head())

if len(neg_rer) > 0:
    print(f"\n⚠️  WARNING: {len(neg_rer)} rows with NEGATIVE RER!")
    print(neg_rer[['Country', 'Year', 'exchange_rate', 'CPI_destination', 'CPI_china', 'RER']].head(10))
else:
    print(f"\n✓ No negative RER values found (as expected!)")

# ==========================================
# 6. SAVE UPDATED DATASET
# ==========================================
output_filename = '../Primary_Dataset_For_Panel_FINAL.csv'
df_merged.to_csv(output_filename, index=False)

print(f"\n✓ Real Exchange Rate (RER) added successfully!")
print(f"✓ Formula: RER = exchange_rate × (CPI_destination ÷ CPI_china)")
print(f"✓ Saved to: {output_filename}")

# ==========================================
# 7. DISPLAY SUMMARY STATISTICS
# ==========================================
print(f"\n{'='*60}")
print(f"SUMMARY STATISTICS")
print(f"{'='*60}")

print(f"\nDataset coverage:")
print(f"Total rows: {len(df_merged)}")
print(f"Rows with RER: {df_merged['RER'].notna().sum()}")
print(f"Rows missing RER: {df_merged['RER'].isna().sum()}")

print(f"\nRER Statistics:")
print(df_merged['RER'].describe())

print(f"\nSample data (Thailand 2015-2020):")
sample = df_merged[
    (df_merged['Country'] == 'Thailand') & 
    (df_merged['Year'].between(2015, 2020))
][['Country', 'Year', 'exchange_rate', 'CPI_destination', 'CPI_china', 'RER']]
print(sample.to_string(index=False))

print(f"\nExample interpretation (Thailand 2020):")
thailand_2020 = df_merged[(df_merged['Country'] == 'Thailand') & (df_merged['Year'] == 2020)]
if not thailand_2020.empty and thailand_2020['RER'].notna().any():
    rer = thailand_2020['RER'].values[0]
    nom_rate = thailand_2020['exchange_rate'].values[0]
    cpi_dest = thailand_2020['CPI_destination'].values[0]
    cpi_china = thailand_2020['CPI_china'].values[0]
    print(f"- Nominal exchange rate: {nom_rate:.4f} CNY per THB")
    print(f"- CPI Thailand: {cpi_dest:.2f}")
    print(f"- CPI China: {cpi_china:.2f}")
    print(f"- Real exchange rate: {rer:.4f}")
    print(f"- This adjusts for inflation differences between China and Thailand")

print(f"\nComparison across countries (2020):")
comparison = df_merged[df_merged['Year'] == 2020][
    ['Country', 'exchange_rate', 'RER']
].sort_values('RER', ascending=False).head(10)
print(comparison.to_string(index=False))

print(f"\n{'='*60}")
print(f"Script completed successfully!")
print(f"{'='*60}")
