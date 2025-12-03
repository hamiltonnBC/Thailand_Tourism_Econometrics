import csv

# Path to the filtered CSV file
input_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/china_thailand_world_bank_data_filtered.csv'
output_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/filtered_reformatted.csv'

# Open and read the filtered CSV file
with open(input_file, 'r', encoding='utf-8') as infile:
    csv_reader = csv.reader(infile)
    
    # Read the header
    headers = next(csv_reader)
    
    # Prepare reformatted data
    reformatted_rows = []
    
    # New header: Country Name, Country Code, Series Name, Series Code, Year, Value
    new_header = ['Country Name', 'Country Code', 'Series Name', 'Series Code', 'Year', 'Value']
    reformatted_rows.append(new_header)
    
    # Iterate through each row
    for row in csv_reader:
        country_name = row[0]
        country_code = row[1]
        series_name = row[2]
        series_code = row[3]
        
        # Iterate through year columns (starting from index 4)
        for i in range(4, len(headers)):
            year = headers[i].split('[')[0].strip()  # Extract year from "1990 [YR1990]"
            value = row[i] if i < len(row) else ''
            
            # Only add row if value is not empty or ".."
            if value and value != '..':
                reformatted_rows.append([country_name, country_code, series_name, series_code, year, value])

with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerows(reformatted_rows)

print(f"Reformatted data saved to: {output_file}")
print(f"Total rows (excluding header): {len(reformatted_rows) - 1}")
