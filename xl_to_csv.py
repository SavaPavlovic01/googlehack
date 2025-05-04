import pandas as pd

# --- Configuration ---
EXCEL_FILE_PATH = 'portali_1_510_prvi_prolaz.xlsm' # --- > Replace with the path to YOUR Excel file (e.g., the one created by merging)
OUTPUT_CSV_PATH = 'extracted_data.csv'      # --- > Choose a name for the NEW output CSV file

# --- > List the EXACT names of the columns you want to keep.
# --- > Make sure these names match the column headers in your Excel file exactly (case-sensitive!).
COLUMNS_TO_KEEP = [
    'Komentar',         
    'Ocena' ,
    'Kljucne reci'
]

# --- Load the Excel file ---
try:
    # You might need to install 'openpyxl': pip install openpyxl
    df = pd.read_excel(EXCEL_FILE_PATH)
    print(f"Successfully loaded '{EXCEL_FILE_PATH}'. Shape: {df.shape}")
    print("Original columns:", df.columns.tolist())

    # --- Check if all specified columns exist ---
    missing_cols = [col for col in COLUMNS_TO_KEEP if col not in df.columns]
    if missing_cols:
        print("\nError: The following specified columns were NOT found in the Excel file:")
        for col in missing_cols:
            print(f"- '{col}'")
        print("\nPlease check the column names in the 'COLUMNS_TO_KEEP' list and the Excel file.")
        exit() # Stop the script if columns are missing

    # --- Select only the desired columns ---
    df_selected = df[COLUMNS_TO_KEEP]
    print(f"\nSelected the following columns: {COLUMNS_TO_KEEP}")
    print("Shape of selected data:", df_selected.shape)

    # --- Save the selected data to a CSV file ---
    # index=False prevents pandas from writing the DataFrame index as a column in the CSV
    # encoding='utf-8' is generally a good choice for text data, especially non-English text
    df_selected.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\nSuccessfully saved the selected columns to '{OUTPUT_CSV_PATH}'.")

except FileNotFoundError:
    print(f"Error: The file '{EXCEL_FILE_PATH}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")