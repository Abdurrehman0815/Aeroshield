import pandas as pd

# Load your dataset (assuming it's a CSV file)
df = pd.read_csv('city_hour.csv')  # Replace with your actual file path

# Step 1: Remove specific columns (PM2.5, PM10, NO, NO2, SO2, O3)
columns_to_remove = ["PM2.5", "PM10", "NO", "NO2", "SO2", "O3","NOx"]
df_cleaned = df.drop(columns=columns_to_remove)

# Step 2: Add a new column "VOC" as the average of Benzene, Toluene, Xylene
df_cleaned['VOC'] = df[['Benzene', 'Toluene', 'Xylene']].mean(axis=1)

# Step 3: Optionally remove Benzene, Toluene, and Xylene after averaging if needed
df_cleaned = df_cleaned.drop(columns=["Benzene", "Toluene", "Xylene"])
def categorize_aqi(aqi_bucket):
    if aqi_bucket in ['Good', 'Satisfactory']:
        return 2
    elif aqi_bucket in ['Moderate', 'Poor']:
        return 1
    elif aqi_bucket in ['Very Poor', 'Severe']:
        return 0
    else:
        return -1

# Apply the function to the AQI_Bucket column
df_cleaned['AQI_Bucket'] = df_cleaned['AQI_Bucket'].apply(categorize_aqi)
df_cleaned = df_cleaned.dropna()
# Save the cleaned data to a new CSV file if needed
df_cleaned.to_csv('cleaned_dataset.csv', index=False)

# Print or display the cleaned dataset
print(df_cleaned.head())
