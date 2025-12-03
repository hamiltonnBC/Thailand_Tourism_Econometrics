import pandas as pd

# Load the CSV
df = pd.read_csv('final_regressions/Primary_Dataset_For_Panel_FINAL.csv')

# Sort by Country and Year
df_sorted = df.sort_values(['Country', 'Year'])

# Save back to the same file
df_sorted.to_csv('final_regressions/Primary_Dataset_For_Panel_FINAL.csv', index=False)

print(f"CSV sorted by Country and Year")
print(f"Total rows: {len(df_sorted)}")
