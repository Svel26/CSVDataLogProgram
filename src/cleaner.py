import os
import time
import json
import pandas as pd
import csv
import logging
import sys

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def remove_rt_count_lines(input_file):
    temp_dir = 'temp_files'
    os.makedirs(temp_dir, exist_ok=True)
    temp_file = os.path.join(temp_dir, os.path.basename(input_file) + ".tmp")
    try:
        with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
            for line in infile:
                if "$RT_COUNT$" not in line:
                    outfile.write(line)
        logging.info(f"Temporary file created at {temp_file}")
    except Exception as e:
        logging.error(f"Error processing {input_file}: {e}")
    return temp_file

def standardize_time_format(time_string):
    try:
        return pd.to_datetime(time_string, dayfirst=True).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logging.error(f"Error parsing date: {time_string} - {e}")
        return time_string

def standardize_csv(temp_file, output_file):
    try:
        df = pd.read_csv(temp_file, delimiter=';')
    except Exception as e:
        logging.error(f"Error reading {temp_file}: {e}")
        return

    logging.info(f"Rows read from {temp_file}: {len(df)}")

    required_columns = ['VarValue', 'Time_ms', 'Validity', 'TimeString']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"Missing columns in {temp_file}: {', '.join(missing_columns)}")
        return

    df.replace({',': '.'}, regex=True, inplace=True)
    df['VarValue'] = pd.to_numeric(df['VarValue'], errors='coerce')
    df['Time_ms'] = pd.to_numeric(df['Time_ms'], errors='coerce')
    df['Validity'] = pd.to_numeric(df['Validity'], errors='coerce')

    df['TimeString'] = df['TimeString'].apply(standardize_time_format)

    try:
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
        logging.info(f"Cleaned CSV saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving {output_file}: {e}")

def clean_datalogs_in_directory(input_directory, output_directory, processed_files, output_file_prefix):
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(input_directory):
        input_file = os.path.join(input_directory, filename)
        if input_file in processed_files:
            logging.info(f"Skipping already processed file: {input_file}")
            continue

        logging.info(f"Processing file: {input_file}")
        temp_file = remove_rt_count_lines(input_file)
        output_file = os.path.join(output_directory, f"{output_file_prefix}_{filename}")
        standardize_csv(temp_file, output_file)
        processed_files.add(input_file)