import pandas as pd

# Load the dataset (modify the file path to your specific dataset)
file_path = 'recieved_data_from_bluetooth.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Step 1: Define a function to calculate AQI subindex for each pollutant
def calculate_aqi_subindex(value, breakpoints):
    """Function to calculate AQI subindex based on pollutant value and given breakpoints."""
    for bp in breakpoints:
        if bp['low'] <= value <= bp['high']:
            aqi = ((bp['aqi_high'] - bp['aqi_low']) / (bp['high'] - bp['low'])) * (value - bp['low']) + bp['aqi_low']
            return round(aqi)
    return None  # For values outside range

# Step 2: Define AQI breakpoints for CO2, NH3, and VOC
co2_breakpoints = [
    {'low': 0, 'high': 600, 'aqi_low': 0, 'aqi_high': 100},   # Good
    {'low': 601, 'high': 1000, 'aqi_low': 101, 'aqi_high': 200},  # Moderate
    {'low': 1001, 'high': 2400, 'aqi_low': 251, 'aqi_high': 400}  # Poor
]

nh3_breakpoints = [
    {'low': 0, 'high': 10, 'aqi_low': 0, 'aqi_high': 100},   # Good
    {'low': 11, 'high': 20, 'aqi_low': 101, 'aqi_high': 250},  # Moderate
    {'low': 20, 'high': 50, 'aqi_low': 251, 'aqi_high': 400}  # Poor
]

voc_breakpoints = [
    {'low': 0, 'high': 50, 'aqi_low': 0, 'aqi_high': 100},    # Good
    {'low': 51, 'high': 100, 'aqi_low': 101, 'aqi_high': 200},  # Moderate
    {'low': 101, 'high': 220, 'aqi_low': 251, 'aqi_high': 400} # Poor
]

# Step 3: Calculate AQI sub-index for each pollutant
df['AQI_CO2'] = df['CO2 (ppm)'].apply(lambda x: calculate_aqi_subindex(x, co2_breakpoints))
df['AQI_NH3'] = df['NH3 (ppm)'].apply(lambda x: calculate_aqi_subindex(x, nh3_breakpoints))
df['AQI_VOC'] = df['VOC (ppm)'].apply(lambda x: calculate_aqi_subindex(x, voc_breakpoints))

# Step 4: Calculate overall AQI (the maximum of the three sub-indices)
df['Overall_AQI'] = df[['AQI_CO2', 'AQI_NH3', 'AQI_VOC']].max(axis=1)

# Step 5: Classify AQI into "Good", "Moderate", and "Poor"
def classify_aqi(aqi):
    if aqi <= 50:
        return 'Good'
    elif 51 <= aqi <= 100:
        return 'Moderate'
    else:
        return 'Poor'

df['AQI_Bucket'] = df['Overall_AQI'].apply(classify_aqi)

# Step 6: Save the modified dataset with AQI values and classification
output_file_path = 'data_with_aqi.csv'  # Modify this path if needed
df.to_csv(output_file_path, index=False)

# Step 7: Print the first few rows of the dataset to verify the results
print(df[['CO2 (ppm)', 'NH3 (ppm)', 'VOC (ppm)', 'AQI_CO2', 'AQI_NH3', 'AQI_VOC', 'Overall_AQI', 'AQI_Bucket']].head())
