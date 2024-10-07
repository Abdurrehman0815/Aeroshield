import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt  # For plotting graphs
from sklearn.model_selection import train_test_split
from sklearnex import patch_sklearn  # Intel oneDAL integration
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error  # Import accuracy score and mean squared error

# Load the training dataset (cleaned_dataset.csv)
file_path_train = 'cleaned_dataset.csv'  # Update with the actual file path
print("Loading training data...")
train_data = pd.read_csv(file_path_train)
print("Training data loaded successfully!")

# Preprocess the training data
print("Preprocessing training data...")
train_data['Datetime'] = pd.to_datetime(train_data['Datetime'], format='%Y-%m-%d %H:%M:%S')
train_data['Hour'] = train_data['Datetime'].dt.hour
train_data['Day'] = train_data['Datetime'].dt.day
train_data['Month'] = train_data['Datetime'].dt.month
train_data['Year'] = train_data['Datetime'].dt.year
print("Training data preprocessing complete.")

# Define features and target for training
train_features = train_data[['AQI', 'Hour', 'Day', 'Month']]  # Features
train_target_aqi = train_data['AQI']  # AQI target for regression
train_target_aqi_bucket = train_data['AQI_Bucket']  # Target (AQI bucket)

# Split the training dataset into training and testing sets for both regression and classification
print("Splitting training data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(train_features, train_target_aqi, test_size=0.2, random_state=42)
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(train_features, train_target_aqi_bucket,
                                                                            test_size=0.2, random_state=42)
print("Training data split complete.")

# Train a Random Forest Regressor with Sklearn for AQI prediction
print("Training Random Forest Regressor with Sklearn...")
start_time = time.time()
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)
sklearn_regressor_time = time.time() - start_time
print(f"Sklearn Regressor Training Time: {sklearn_regressor_time:.4f} seconds")

# Train a Random Forest Classifier with Sklearn for AQI bucket classification
print("Training Random Forest Classifier with Sklearn...")
start_time = time.time()
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_class, y_train_class)
sklearn_classifier_time = time.time() - start_time
print(f"Sklearn Classifier Training Time: {sklearn_classifier_time:.4f} seconds")

# Patch sklearn to use Intel oneDAL for better performance
patch_sklearn()

# Train a Random Forest Regressor with Intel oneDAL (sklearnex)
print("Training Random Forest Regressor with Intel oneDAL (sklearnex)...")
start_time = time.time()
rf_regressor_ex = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor_ex.fit(X_train, y_train)
intel_regressor_time = time.time() - start_time
print(f"Intel Regressor Training Time: {intel_regressor_time:.4f} seconds")

# Train a Random Forest Classifier to classify AQI buckets using the training data
print("Training Random Forest Classifier with Intel oneDAL (sklearnex)...")
start_time = time.time()
rf_classifier_ex = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier_ex.fit(X_train_class, y_train_class)
intel_classifier_time = time.time() - start_time
print(f"Intel Classifier Training Time: {intel_classifier_time:.4f} seconds")

# Load and preprocess the input data (air_quality_with_aqi.csv)
file_path_input = 'air_quality_with_aqi.csv'  # Update with the actual file path
print("Loading input data for prediction...")
input_data = pd.read_csv(file_path_input)
print("Input data loaded successfully!")

# Get the current system time for Hour, Day, and Month
now = datetime.now()
current_hour = now.hour
current_day = now.day
current_month = now.month
print(f"Current system time: Hour={current_hour}, Day={current_day}, Month={current_month}")

# Function to predict AQI and AQI bucket for the next 24 hours using the current system time
def predict_aqi_for_next_24_hours(last_known_aqi):
    bucket_predictions = []  # Initialize the list here
    aqi_predictions = []  # List to store AQI predictions

    # Predict for the next 24 hours
    for hour_offset in range(25):  # From current hour to the next 24 hours
        hour = (current_hour + hour_offset) % 24  # Wrap around after 23
        day = current_day + (current_hour + hour_offset) // 24  # Increment day if needed
        month = current_month

        # Prepare input for the model
        input_data = pd.DataFrame([[last_known_aqi, hour, day, month]], columns=['AQI', 'Hour', 'Day', 'Month'])

        # Predict the AQI bucket using the classifier
        bucket_prediction = rf_classifier_ex.predict(input_data)[0]

        # Store the predictions
        bucket_predictions.append((hour, day, month, bucket_prediction))
        aqi_predictions.append((hour, day, month, last_known_aqi))  # Assuming last_known_aqi for now

        # Logic to estimate the next AQI value can be added here, for example:
        last_known_aqi += 1  # Simulate an increment (this is just an example)

    return bucket_predictions, aqi_predictions

# Get the last known AQI value from the input data
last_known_aqi = input_data['Overall_AQI'].iloc[-1]

# Predict AQI bucket and value for the next 24 hours
bucket_predictions, aqi_predictions = predict_aqi_for_next_24_hours(last_known_aqi)

# Display predictions
print("\nAQI Bucket Predictions for the next 24 hours:")
for (hour, day, month, bucket), (aqi_hour, aqi_day, aqi_month, aqi) in zip(bucket_predictions, aqi_predictions):
    print(f"Hour {hour}, Day {day}, Month {month}: Predicted AQI: {aqi:.2f}, Predicted AQI Bucket: {bucket}")

# Find the peak AQI value predicted for the next 24 hours
peak_prediction = max(zip(aqi_predictions, bucket_predictions), key=lambda x: x[0][3])  # Assuming AQI is the third value
peak_aqi_hour, peak_aqi_day, peak_aqi_month, peak_aqi = peak_prediction[0]
peak_bucket_hour, peak_bucket_day, peak_bucket_month, peak_bucket = peak_prediction[1]

print(f"\nPeak Prediction: Hour {peak_aqi_hour}, Day {peak_aqi_day}, Month {peak_aqi_month} with Predicted AQI: {peak_aqi:.2f}, AQI Bucket: {peak_bucket}")

# Calculate accuracy for Intel oneDAL models
y_pred_class = rf_classifier_ex.predict(X_test_class)
accuracy_intel_classifier = accuracy_score(y_test_class, y_pred_class) * 100  # Convert to percentage
print(f"Accuracy for Intel Classifier: {accuracy_intel_classifier:.2f}%")  # Print accuracy as percentage

# Summary of results (with four training times)
print("\nSummary of Results:")
print(f"Sklearn Regressor Training Time: {sklearn_regressor_time:.4f} seconds")
print(f"Sklearn Classifier Training Time: {sklearn_classifier_time:.4f} seconds")
print(f"Intel Regressor Training Time: {intel_regressor_time:.4f} seconds")
print(f"Intel Classifier Training Time: {intel_classifier_time:.4f} seconds")
print(f"Intel Classifier Accuracy: {accuracy_intel_classifier:.2f}%")  # Include accuracy in summary

# Generate a bar chart for training times
def plot_training_times():
    models = ['Sklearn Regressor', 'Sklearn Classifier', 'Intel Regressor', 'Intel Classifier']
    training_times = [sklearn_regressor_time, sklearn_classifier_time, intel_regressor_time, intel_classifier_time]

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(models, training_times, color=['blue', 'green', 'red', 'orange'])
    plt.xlabel('Models')
    plt.ylabel('Training Time (seconds)')
    plt.title('Training Times for Sklearn and Intel oneDAL Models')
    plt.show()

# Call the function to plot the graph
plot_training_times()
