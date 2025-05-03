import pandas as pd
import cyrtranslit
import os

# --- Configuration ---
# Replace 'your_input_file.xlsx' with the actual path to your Excel file
INPUT_FILE_PATH = 'D2.1a.Recnik_pogrdnih_naziva_po_kategorijama.xlsx'
# Replace 'output_latin_file.xlsx' with the desired name for the converted file
OUTPUT_FILE_PATH = 'D2.1a.Recnik_pogrdnih_naziva_po_kategorijama_latin.xlsx'
# --- End Configuration ---

def transliterate_serbian_cyrillic_to_latin(text):
    """
    Transliterates a string from Serbian Cyrillic to Serbian Latin.
    If the input is not a string or if an error occurs, returns the original input.
    """
    if isinstance(text, str):
        try:
            # Use 'sr' for Serbian language rules
            return cyrtranslit.to_latin(text, 'sr')
        except Exception as e:
            # print(f"Warning: Could not transliterate '{text[:50]}...': {e}")
            return text # Return original text if conversion fails
    return text # Return non-string data as is (numbers, dates, etc.)

def convert_excel_cyrillic_to_latin(input_path, output_path):
    """
    Reads an Excel file, converts all string cells from Serbian Cyrillic
    to Serbian Latin across all sheets, and saves to a new file.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    print(f"Reading Excel file: '{input_path}'...")
    try:
        # Read all sheets into a dictionary of DataFrames
        # sheet_name=None reads all sheets
        excel_data = pd.read_excel(input_path, sheet_name=None)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    print("Processing sheets and converting text...")
    processed_sheets = {}
    for sheet_name, df in excel_data.items():
        print(f"  Processing sheet: '{sheet_name}'...")
        # Apply the transliteration function to every cell in the DataFrame
        # The .map() function (pandas >= 2.1.0) applies element-wise.
        # Our transliterate function handles non-string types gracefully.
        # For older pandas versions, df.applymap(transliterate_serbian_cyrillic_to_latin) might be used.
        try:
            processed_sheets[sheet_name] = df.map(transliterate_serbian_cyrillic_to_latin)
        except AttributeError:
             # Fallback for older pandas versions that might not have .map on DataFrame
             print("    (Using fallback applymap for older pandas version)")
             processed_sheets[sheet_name] = df.applymap(transliterate_serbian_cyrillic_to_latin)


    print(f"Writing converted data to: '{output_path}'...")
    try:
        # Use ExcelWriter to save multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, processed_df in processed_sheets.items():
                # Write each processed DataFrame to its corresponding sheet
                # index=False prevents writing the DataFrame index as a column
                processed_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print("Conversion complete!")
    except Exception as e:
        print(f"Error writing Excel file: {e}")

# --- Run the Conversion ---
if __name__ == "__main__":
    convert_excel_cyrillic_to_latin(INPUT_FILE_PATH, OUTPUT_FILE_PATH)