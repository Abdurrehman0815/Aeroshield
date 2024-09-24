import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the cleaned dataset
data_cleaned = pd.read_csv('cleaned_data.csv')

# Drop rows with missing target column (if any)
data_cleaned = data_cleaned.dropna(subset=['AQI_Bucket'])

# Encode categorical columns
data_cleaned['AQI_Bucket'] = data_cleaned['AQI_Bucket'].astype('category').cat.codes

# Define features (X) and target (y)
X = data_cleaned.drop(['AQI_Bucket', 'City', 'Date'], axis=1)
y = data_cleaned['AQI_Bucket']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred) * 100

print(f"Model Accuracy: {accuracy:.2f}%")
