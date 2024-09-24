import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime

# Load the cleaned dataset
data_cleaned = pd.read_csv('cleaned_data.csv')

# Drop rows with missing target column (if any)
data_cleaned = data_cleaned.dropna(subset=['AQI_Bucket'])

# Encode the target 'AQI_Bucket'
data_cleaned['AQI_Bucket'] = data_cleaned['AQI_Bucket'].astype('category').cat.codes

# Define features (X) and target (y)
X = data_cleaned.drop(['AQI_Bucket', 'City', 'Date'], axis=1)
y = data_cleaned['AQI_Bucket']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred) * 100
print(f"Model Accuracy: {accuracy:.2f}%")

# =====================================
# Function to Predict AQI_Bucket for a Future Date and City
# =====================================
def predict_aqi(year, month, day, city):
    # Convert input into a date object
    input_date = datetime(year, month, day)

    # Filter the data for the same month and city to compute average feature values
    data_cleaned['Date'] = pd.to_datetime(data_cleaned['Date'])
    monthly_city_data = data_cleaned[(data_cleaned['Date'].dt.month == month) & (data_cleaned['City'] == city)]

    # Check if there is enough data for the city and month
    if monthly_city_data.empty:
        print(f"No data available for {city} in {input_date.strftime('%B')} {year}.")
        return

    # Compute the average values of the features for the given month and city
    avg_features = monthly_city_data.drop(['AQI_Bucket', 'City', 'Date'], axis=1).mean()

    # Prepare the input data for prediction (reshape it as a single row)
    input_features = np.array(avg_features).reshape(1, -1)

    # Predict the AQI_Bucket using the trained model
    predicted_bucket = model.predict(input_features)

    # Decode the predicted bucket back to the original categories (if needed)
    decoded_bucket = data_cleaned['AQI_Bucket'].astype('category').cat.categories[predicted_bucket[0]]
    
    print(f"Predicted AQI_Bucket for {city} on {input_date.strftime('%Y-%m-%d')}: {decoded_bucket}")

# =====================================
# Find the Most Polluted City
# =====================================
def find_most_polluted_city():
    # Group by city and count the number of 0s in the AQI_Bucket for each city
    polluted_cities = data_cleaned[data_cleaned['AQI_Bucket'] == 0].groupby('City').size()

    # Find the city with the maximum number of 0 values (most polluted)
    most_polluted_city = polluted_cities.idxmax()
    most_polluted_count = polluted_cities.max()

    print(f"Most Polluted City: {most_polluted_city} with {most_polluted_count} records of AQI_Bucket = 0.")

# =====================================
# Predict AQI until 2030 for a given city
# =====================================
def predict_aqi_until_2030(city):
    # Get the latest year from the data
    latest_year = data_cleaned['Date'].dt.year.max()
    
    # Calculate how many years to predict until 2030
    years_to_predict = 2030 - latest_year
    
    if years_to_predict <= 0:
        print(f"The latest data is already from {latest_year}, no need to predict beyond that.")
        return
    
    # Get the average AQI of the city for each year in the dataset
    city_data = data_cleaned[data_cleaned['City'] == city]
    yearly_aqi = city_data.groupby(city_data['Date'].dt.year)['AQI_Bucket'].mean()
    
    # Calculate the average yearly change in AQI
    avg_increase_per_year = yearly_aqi.diff().mean()
    
    # Predict AQI for the years until 2030
    future_years = list(range(latest_year + 1, 2031))
    
    # Predict AQI values for each future year
    future_aqi = [yearly_aqi.iloc[-1] + avg_increase_per_year * (i + 1) for i in range(years_to_predict)]
    
    # Plot the historical and predicted data
    plt.figure(figsize=(10, 6))
    
    # Plot historical data
    plt.plot(yearly_aqi.index, yearly_aqi.values, label="Historical AQI", marker='o')
    
    # Plot future predictions
    plt.plot(future_years, future_aqi, label="Predicted AQI", marker='x', linestyle='--')
    
    # Set plot labels and title
    plt.xlabel('Year')
    plt.ylabel('Average AQI')
    plt.title(f'AQI Predictions for {city} until 2030')
    plt.legend()
    
    # Show the graph
    plt.grid(True)
    plt.show()

# =====================================
# Get user input and predict AQI for a city and date
# =====================================
a = int(input("Enter the Date (DD): "))
b = int(input("Enter the Month (MM): "))
c = int(input("Enter the Year (YYYY): "))
city = input("Enter the City: ")

# Predict AQI for the given date and city
predict_aqi(c, b, a, city)

# =====================================
# Predict AQI until 2030 for the given city
# =====================================
predict_aqi_until_2030(city)

# =====================================
# Find and display the most polluted city
# =====================================
find_most_polluted_city()
