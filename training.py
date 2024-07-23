import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os


file_path = 'weather_power.csv'
print(f"Checking file: {file_path}")
print("File exists:", os.path.isfile(file_path))

# Load the data from CSV file
df = pd.read_csv('weather_power.csv')

# Preprocess the data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek

# Features and target variable
X = df[['temperature', 'humidity', 'hour', 'day_of_week']]
y = df['power_consumption']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Predict future power consumption
def predict_power_consumption(temp, hum, hour, day_of_week):
    return model.predict([[temp, hum, hour, day_of_week]])[0]

# Example prediction
future_temp = 25.0  # Example temperature
future_hum = 60.0   # Example humidity
future_hour = 14    # Example hour
future_day_of_week = 2  # Example day of the week
predicted_power = predict_power_consumption(future_temp, future_hum, future_hour, future_day_of_week)
print(f"Predicted Power Consumption: {predicted_power} kWh")

# Cost Calculation
def calculate_cost(power_consumption, rate_per_kwh):
    return power_consumption * rate_per_kwh

# Example calculation
rate_per_kwh = 0.12  # Example rate in USD
predicted_cost = calculate_cost(predicted_power, rate_per_kwh)
print(f"Predicted Cost: ${predicted_cost}")