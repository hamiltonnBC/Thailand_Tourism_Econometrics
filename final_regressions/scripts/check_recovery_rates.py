import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('../Primary_Dataset_For_Panel_FINAL.csv')

# Filter for countries in the model
countries = ['Australia', 'Cambodia', 'Indonesia', 'Japan', 
             'Malaysia', 'Singapore', 'Thailand', 'Viet Nam']
df = df[df['Country'].isin(countries)]

print("="*80)
print("RECOVERY RATE ANALYSIS: Percentage Change from 2019")
print("="*80)

results = []

for country in countries:
    country_data = df[df['Country'] == country].sort_values('Year')
    
    # Get values
    val_2019 = country_data[country_data['Year'] == 2019]['arrivals_from_china'].values
    val_2022 = country_data[country_data['Year'] == 2022]['arrivals_from_china'].values
    val_2023 = country_data[country_data['Year'] == 2023]['arrivals_from_china'].values
    val_2024 = country_data[country_data['Year'] == 2024]['arrivals_from_china'].values
    
    if len(val_2019) > 0:
        baseline = val_2019[0]
        
        # Calculate percentage of 2019 level recovered
        pct_2022 = (val_2022[0] / baseline * 100) if len(val_2022) > 0 else None
        pct_2023 = (val_2023[0] / baseline * 100) if len(val_2023) > 0 else None
        pct_2024 = (val_2024[0] / baseline * 100) if len(val_2024) > 0 else None
        
        # Recovery rate (how much of the gap closed from 2022 to 2024)
        if pct_2022 and pct_2024:
            recovery_rate = pct_2024 - pct_2022
        else:
            recovery_rate = None
        
        results.append({
            'Country': country,
            '2019_Baseline': baseline,
            '2022_%_of_2019': pct_2022,
            '2023_%_of_2019': pct_2023,
            '2024_%_of_2019': pct_2024,
            'Recovery_Rate_2022_to_2024': recovery_rate
        })

# Create DataFrame
results_df = pd.DataFrame(results)

print("\n2019 Baseline (absolute numbers):")
print(results_df[['Country', '2019_Baseline']].to_string(index=False))

print("\n\nRecovery as % of 2019 Level:")
print(results_df[['Country', '2022_%_of_2019', '2023_%_of_2019', '2024_%_of_2019']].to_string(index=False))

print("\n\nRecovery Rate (percentage points gained from 2022 to 2024):")
recovery_sorted = results_df[['Country', 'Recovery_Rate_2022_to_2024']].sort_values('Recovery_Rate_2022_to_2024', ascending=False)
print(recovery_sorted.to_string(index=False))

print("\n" + "="*80)
print("KEY INSIGHT:")
print("="*80)

thailand_recovery = results_df[results_df['Country'] == 'Thailand']['Recovery_Rate_2022_to_2024'].values[0]
avg_recovery = results_df['Recovery_Rate_2022_to_2024'].mean()

print(f"\nThailand's recovery rate (2022→2024): {thailand_recovery:.1f} percentage points")
print(f"Average recovery rate (all countries): {avg_recovery:.1f} percentage points")

if thailand_recovery < avg_recovery:
    print(f"\n⚠️  Thailand IS recovering SLOWER than average by {avg_recovery - thailand_recovery:.1f} pp")
    print("Your intuition was CORRECT!")
else:
    print(f"\n✓ Thailand is recovering FASTER than average by {thailand_recovery - avg_recovery:.1f} pp")
    print("The regression result is confirmed!")

# Check if it's a size effect
print("\n" + "="*80)
print("TESTING FOR SIZE EFFECT:")
print("="*80)
print("\nCorrelation between 2019 baseline size and recovery rate:")
correlation = results_df['2019_Baseline'].corr(results_df['Recovery_Rate_2022_to_2024'])
print(f"Correlation: {correlation:.3f}")

if abs(correlation) > 0.5:
    print("⚠️  Strong correlation detected - larger destinations recover differently!")
else:
    print("✓ No strong size effect - recovery is independent of baseline size")
