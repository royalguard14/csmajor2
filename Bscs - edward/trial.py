import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Read the dataset
csv_path = 'edited.csv'  # Change this to your file's path
df = pd.read_csv(csv_path)

# Drop rows with missing values
df = df.dropna()

# Convert categorical columns into dummy variables (one-hot encoding)
df = pd.get_dummies(df, columns=['age_certification', 'type'])

# Splitting the data into features and target
y = df["merge"]
x = df.drop(["merge", "index"], axis=1)

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)

# Train the Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=5)
rf.fit(X_train, y_train)

print(x.columns)

accuracy_rf = rf.score(X_test, y_test)
print(f"Random Forest Accuracy on Test Set: {accuracy_rf:.2f}")

# Example prediction
data_to_predict = [[1967, 101, 7.7, 111189,0, 0,0, 0,1, 0,0, 0,0, 0,0, 1, 0]]



  # Add values for categorical columns as needed
data_pred_rf = rf.predict(data_to_predict)
print(f"Predicted TikToker Name (Random Forest): {data_pred_rf[0]}")
