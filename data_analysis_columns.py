import csv

# Path to the CSV file
csv_file = 'data/API_Data/P_Data_Extract_From_World_Development_Indicators/china_thailand_world_bank_data.csv'

# Open and read the CSV file
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # Get the header row (first row contains column names)
    headers = next(csv_reader)
    
    # Print all column names
    print("Column names:")
    for i, column_name in enumerate(headers):
        print(f"{i + 1}. {column_name}")
