import pandas as pd
import csv
import os
import time

def remove_rt_count_lines(input_file):
    """Remove lines containing '$RT_COUNT$' and write to a temporary file."""
    temp_file = input_file + '.tmp'
    
    with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
        for line in infile:
            if '$RT_COUNT$' not in line:
                outfile.write(line)

    return temp_file  # Return the path of the temporary file

def standardize_csv(temp_file, output_file):
    # Step 1: Detect the delimiter
    with open(temp_file, 'r') as file:
        sample = file.read(1024)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ','
        print(f"Detected delimiter for {temp_file}: '{delimiter}'")

    # Step 2: Read CSV with detected delimiter
    try:
        df = pd.read_csv(temp_file, delimiter=delimiter)
    except Exception as e:
        print(f"Error reading {temp_file}: {e}")
        return

    # Debugging: Output number of rows read
    print(f"Rows read from {temp_file}: {len(df)}")

    # Step 3: Standardize numeric values (handle decimal commas)
    df.replace({',': '.'}, regex=True, inplace=True)
    df['VarValue'] = pd.to_numeric(df['VarValue'], errors='coerce')
    df['Time_ms'] = pd.to_numeric(df['Time_ms'], errors='coerce')
    df['Validity'] = pd.to_numeric(df['Validity'], errors='coerce')

    # Step 4: Ensure consistent time format
    def standardize_time_format(time_string):
        try:
            return pd.to_datetime(time_string).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error parsing date: {time_string} - {e}")
            return time_string

    df['TimeString'] = df['TimeString'].apply(standardize_time_format)

    # Step 5: Save the cleaned CSV to the specified output file
    try:
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
        print(f"Cleaned CSV saved to {output_file}")
    except Exception as e:
        print(f"Error saving {output_file}: {e}")

def clean_datalogs_in_directory(input_directory, output_directory, processed_files):
    # Process files that contain 'datalog' and end with '.csv'
    for filename in os.listdir(input_directory):
        if "datalog" in filename.lower() and filename.endswith(".csv"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f"cleaned_{filename}")

            # Check if the file has been modified since last processed
            last_modified_time = os.path.getmtime(input_file)

            # Process the file if it is new or has been modified
            if filename not in processed_files or processed_files[filename] < last_modified_time:
                try:
                    print(f"Removing '$RT_COUNT$' lines from: {input_file}")
                    temp_file = remove_rt_count_lines(input_file)  # Remove unwanted lines
                    print(f"Processing file: {input_file}")
                    standardize_csv(temp_file, output_file)
                    processed_files[filename] = last_modified_time
                    
                    # Optionally, delete the temporary file after processing
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Error processing {input_file}: {e}")

def run_cleaner(input_directory, output_directory):
    processed_files = {}

    while True:
        clean_datalogs_in_directory(input_directory, output_directory, processed_files)
        time.sleep(5)

# Usage Example
input_directory_path = r'.\Logs\OriginalLogs'  # Directory containing your datalog files
output_directory_path = r'.\Logs\CleanedLogs'  # Directory to save cleaned files

# Create input and output directories if they don't exist
os.makedirs(input_directory_path, exist_ok=True)
os.makedirs(output_directory_path, exist_ok=True)

run_cleaner(input_directory_path, output_directory_path)
