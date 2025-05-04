import pandas as pd

# Read CSV without headers
df = pd.read_csv("D2.1b.Recnik_narodnih_pogrdnih_izraza.csv", header=None, delimiter=',', on_bad_lines='skip')


# Extract the first column
first_column = df.iloc[:, 0]

keywords = first_column_list = df.iloc[:, 0].dropna().tolist()

df = pd.DataFrame(keywords)

# Save to CSV
df.to_csv("keywords.csv", index=False, header=False)