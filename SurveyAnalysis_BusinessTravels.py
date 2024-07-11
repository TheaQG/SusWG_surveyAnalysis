import pandas as pd

# Load the CSV file
file_path = 'csv/example.csv'
data = pd.read_csv(file_path)

# Read the raw content of the file to understand its structure
with open(file_path, 'r') as file:
    raw_content = file.read()

# Split raw content into lines
lines = raw_content.split('\n')

# Filter out empty lines
non_empty_lines = [line for line in lines if line.strip() != '']

# Identify the header row (assuming the first non-empty line has the correct headers)
header_row = non_empty_lines[0]
header_columns = header_row.split(';')

# Determine the maximum number of columns to filter out incomplete rows
column_counts = [len(line.split(';')) for line in non_empty_lines]
max_columns = max(column_counts)

# Filter out rows that don't match the expected number of columns
filtered_data = [line.split(';') for line in non_empty_lines if len(line.split(';')) == max_columns]

# Create a DataFrame using the filtered data
cleaned_df = pd.DataFrame(filtered_data, columns=header_columns)

# Set the first row as the header
cleaned_df.columns = cleaned_df.iloc[0]
cleaned_df = cleaned_df[1:]

# Copy the cleaned DataFrame with all columns
full_df = cleaned_df.copy()

print(full_df.head())
# # Display the full DataFrame with all columns
# import ace_tools as tools; tools.display_dataframe_to_user(name="Full DataFrame", dataframe=full_df)
# full_df.head()
