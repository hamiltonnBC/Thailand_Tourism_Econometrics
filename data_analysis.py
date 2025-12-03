import csv

# Path to the CSV file
csv_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/china_thailand_world_bank_data.csv'

# Open and read the CSV file
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # Iterate through each row
    for row in csv_reader:
        # Print column 3 (index 2) and column 4 (index 3)
        if len(row) >= 4:
            print(f"Column 3: {row[2]}, Column 4: {row[3]}")
