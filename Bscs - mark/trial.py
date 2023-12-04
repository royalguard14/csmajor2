import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Read the dataset
csv_path = 'tii.csv'  # Change this to your file's path
df = pd.read_csv(csv_path).fillna('')

# Splitting the data into features and target
y = df["Tiktoker name"]
x = df.drop(["Tiktoker name", "S.no"], axis=1)

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=5)
rf.fit(X_train_scaled, y_train)

# Testing the Random Forest model
accuracy_rf = rf.score(X_test_scaled, y_test)
print(f"Random Forest Accuracy on Test Set after Scaling: {accuracy_rf:.2f}")

# Make predictions with Random Forest
data_to_predict = [[5500000,802300,1600,4400,5500000]]
data_to_predict_scaled = scaler.transform(data_to_predict)
data_pred_rf = rf.predict(data_to_predict_scaled)
print(f"Predicted TikToker Name (Random Forest): {data_pred_rf[0]}")
