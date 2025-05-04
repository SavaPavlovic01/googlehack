import pandas as pd
import cyrtranslit
import openpyxl
import os

# --- Configuration ---
# 1. Specify the path to your input Excel file
INPUT_EXCEL_PATH = 'D2.1a.Recnik_pogrdnih_naziva_po_kategorijama.xlsx'

# 2. Specify the sheet name OR index (0 for the first sheet, 1 for second, etc.)
#    If using name: SHEET_IDENTIFIER = 'Sheet1'
#    If using index: SHEET_IDENTIFIER = 0
SHEET_IDENTIFIER = 6 # Example: using the first sheet (index 0)

# 3. Specify the column index (0 for first column, 1 for second, etc.)
COLUMN_INDEX_TO_EXTRACT = 0 # Second column


# 5. Specify the desired path for the output CSV file
OUTPUT_CSV_PATH = 'keywords.csv'
# --- End Configuration ---

def transliterate_serbian_cyrillic_to_latin(text):
    """
    Transliterates a string from Serbian Cyrillic to Serbian Latin.
    Handles non-string types and potential errors.
    """
    if isinstance(text, str):
        try:
            # Use 'sr' for Serbian language rules
            return cyrtranslit.to_latin(text, 'sr')
        except Exception as e:
            # print(f"Warning: Could not transliterate '{str(text)[:50]}...': {e}")
            return str(text) # Return original as string if conversion fails
    # If it's not a string initially (like NaN, numbers), convert to string
    # or handle as needed. Here we convert potential non-strings to empty strings
    # if they are NaN, otherwise convert to string representation.
    if pd.isna(text):
        return ""
    return str(text)

def process_excel_column_to_csv(input_excel, sheet_id, col_index, output_csv):
    """
    Reads a specific column from an Excel sheet, converts text to Latin,
    appends words, and saves to CSV.
    """
    if not os.path.exists(input_excel):
        print(f"Error: Input Excel file not found at '{input_excel}'")
        return

    print(f"Reading sheet '{sheet_id}' from '{input_excel}'...")
    try:
        # Read the specific sheet
        df = pd.read_excel(input_excel, sheet_name=sheet_id)
    except Exception as e:
        print(f"Error reading Excel file or sheet: {e}")
        return

    # Check if the column index is valid
    if col_index < 0 or col_index >= len(df.columns):
        print(f"Error: Column index {col_index} is out of bounds for sheet '{sheet_id}'.")
        print(f"Available columns: {len(df.columns)}")
        return

    print(f"Extracting data from column index {col_index}...")
    # Select the specific column using iloc for integer-location based indexing
    # .dropna() removes empty cells, .astype(str) ensures all are strings
    try:
        extracted_column_data = df.iloc[:, col_index].dropna().astype(str).tolist()
    except IndexError:
         print(f"Error: Could not access column at index {col_index}.")
         return


    print("Converting extracted text to Serbian Latin...")
    converted_list = [transliterate_serbian_cyrillic_to_latin(item) for item in extracted_column_data]

    print("Adding extra words (and ensuring they are Latin)...")


    # Combine the lists
    final_list = converted_list 
    for l in final_list:
        print(l)

    print(f"Saving the final list to '{output_csv}'...")
    try:
        output_df = pd.DataFrame(final_list)

        # Check if the CSV file already exists to determine the write mode
        file_exists = os.path.exists(output_csv)

        # Use mode 'a' (append) if the file exists, 'w' (write) otherwise.
        # Always use header=False to avoid writing column names.
        write_mode = 'a' if file_exists else 'w'
        write_header = False # Never write header as per request
        output_df.to_csv(
            output_csv,
            mode=write_mode,    # 'a' for append, 'w' for write new
            header=write_header,# Set to False to never write the header
            index=False,        # Do not write DataFrame index
            encoding='utf-8'    # Use UTF-8 encoding
        )

        print(f"Data successfully {'appended to' if file_exists else 'written to'} '{output_csv}'!")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# --- Run the Process ---
if __name__ == "__main__":
    process_excel_column_to_csv(
        INPUT_EXCEL_PATH,
        SHEET_IDENTIFIER,
        COLUMN_INDEX_TO_EXTRACT,
        OUTPUT_CSV_PATH
    )