import pandas as pd

# Load the dataset
data = pd.read_csv('city_day.csv')

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Drop rows where all values (except 'City' and 'Date') are NaN
data_cleaned = data.dropna(how='all', subset=data.columns.difference(['City', 'Date']))

# Fill missing numeric columns with the mean value
numeric_columns = data_cleaned.select_dtypes(include=['float64', 'int64']).columns
data_cleaned[numeric_columns] = data_cleaned[numeric_columns].fillna(data_cleaned[numeric_columns].mean())

# Remove duplicate rows if any
data_cleaned = data_cleaned.drop_duplicates()

# Save the cleaned data to a new file
data_cleaned.to_csv('cleaned_data.csv', index=False)

# Check for remaining missing values
print(data_cleaned.isnull().sum())
