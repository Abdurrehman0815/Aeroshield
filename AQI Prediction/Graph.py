import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix

# Load the cleaned dataset
data_cleaned = pd.read_csv('cleaned_data.csv')

# Drop rows with missing target column (if any)
data_cleaned = data_cleaned.dropna(subset=['AQI_Bucket'])

# Encode categorical target 'AQI_Bucket'
data_cleaned['AQI_Bucket'] = data_cleaned['AQI_Bucket'].astype('category').cat.codes

# Define features (X) and target (y)
X = data_cleaned.drop(['AQI_Bucket', 'City', 'Date'], axis=1)
y = data_cleaned['AQI_Bucket']

# Split the dataset into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred) * 100
print(f"Model Accuracy: {accuracy:.2f}%")

# =====================================
# 1. Feature Importance Graph
# =====================================
importances = model.feature_importances_
feature_names = X.columns

# Sort the importances and plot
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10,6))
plt.title("Feature Importance")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), feature_names[indices], rotation=90)
plt.tight_layout()
plt.show()

# =====================================
# 2. Confusion Matrix Graph
# =====================================
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot using Seaborn
plt.figure(figsize=(8,6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.show()

# =====================================
# 3. Cross-Validation Scores Graph
# =====================================
cv_scores = cross_val_score(model, X, y, cv=5)

# Plot the cross-validation scores
plt.figure(figsize=(6,4))
plt.plot(range(1, 6), cv_scores, marker='o')
plt.title("Cross-Validation Scores")
plt.xlabel("Fold")
plt.ylabel("Accuracy")
plt.show()

# Print average cross-validation score
print(f"Average Cross-Validation Score: {cv_scores.mean() * 100:.2f}%")
