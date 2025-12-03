import pandas as pd

# Read the CSV file
csv_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/filtered_reformatted.csv'
xlsx_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/filtered_reformatted.xlsx'

# Load CSV
df = pd.read_csv(csv_file)

# Save as Excel
df.to_excel(xlsx_file, index=False, sheet_name='Data')

print(f"Successfully converted CSV to Excel!")
print(f"Output file: {xlsx_file}")
print(f"Total rows: {len(df)}")
