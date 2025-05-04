import pandas as pd
import numpy as np # Often useful with pandas, though not strictly needed for this specific logic
import os # To check if files exist

# --- Configuration ---

# --- > List the paths to the THREE input CSV files
CSV_FILE_PATHS = [
    'extracted_data.csv',
    'extracted_data1.csv',
    'extracted_data2.csv'
]

# --- > Specify the name of the column you want to modify
# --- > Make sure this column name exists in ALL (or at least some) of your CSVs.
COLUMN_TO_TRANSFORM = 'Ocena' # e.g., 'hatespeech category', 'label' etc.

# --- > Specify the path for the final merged and modified output CSV file
OUTPUT_CSV_PATH = 'hate_speech_data.csv'

# List to hold the individual DataFrames
dfs_list = []

print("--- Loading CSV Files ---")
all_files_found = True
for file_path in CSV_FILE_PATHS:
    try:
        df = pd.read_csv(file_path)
        dfs_list.append(df)
        print(f"Successfully loaded '{file_path}'. Shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'. Please check the path.")
        all_files_found = False
    except Exception as e:
        print(f"Error loading '{file_path}': {e}")
        all_files_found = False

# Only proceed if all files were loaded successfully
if not all_files_found:
    print("\nAborting script because one or more input files could not be loaded.")
else:
    # --- Merge (Concatenate) the DataFrames ---
    print("\n--- Merging DataFrames ---")
    # ignore_index=True creates a new continuous index for the merged DataFrame
    combined_df = pd.concat(dfs_list, ignore_index=True)
    print(f"Successfully merged {len(dfs_list)} files.")
    print(f"Shape of combined DataFrame: {combined_df.shape}")

    # --- Transform the specified column ---
    print(f"\n--- Transforming Column: '{COLUMN_TO_TRANSFORM}' ---")

 

    # --- Save the final DataFrame to a new CSV file ---
    print(f"\n--- Saving Merged and Transformed Data ---")
    try:
        # index=False prevents pandas from writing the DataFrame index as a column in the CSV
        # encoding='utf-8' is generally recommended
        combined_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print(f"Successfully saved the final data to '{OUTPUT_CSV_PATH}'.")
    except Exception as e:
        print(f"Error saving file '{OUTPUT_CSV_PATH}': {e}")

print("\n--- Script Finished ---")