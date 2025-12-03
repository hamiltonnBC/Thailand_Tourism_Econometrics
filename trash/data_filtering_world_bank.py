import csv

# Path to the CSV file
csv_file = '../data/API_Data/P_Data_Extract_From_World_Development_Indicators/china_thailand_world_bank_data.csv'
output_file = '../data/API_Data/P_Data_Extract_From_World_Development_Indicators/china_thailand_world_bank_data_filtered.csv'

# Series codes to keep
series_codes_to_keep = [
    "NY.GDP.MKTP.CD",      # GDP current US$
    "NY.GDP.MKTP.KD.ZG",   # GDP growth %
    "NY.GDP.PCAP.CD",      # GDP per capita
    "FP.CPI.TOTL.ZG",      # Inflation (CPI)
    "SP.POP.TOTL"          # Population
]

with open(csv_file, 'r', encoding='utf-8') as infile:
    csv_reader = csv.reader(infile)
    
    headers = next(csv_reader)
    
    filtered_rows = [headers]
    
    for row in csv_reader:
        # Checking if column 4 (index 3) matches any of the series codes
        if len(row) >= 4 and row[3] in series_codes_to_keep:
            filtered_rows.append(row)

with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerows(filtered_rows)

print(f"Filtered data saved to: {output_file}")
print(f"Total rows kept (excluding header): {len(filtered_rows) - 1}")
