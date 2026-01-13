import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# 1. Locate the file
# This finds train.csv in the folder above 'scripts'
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'train.csv')

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found! Check your root directory.")
    exit()

# 2. Load the CSV data
df = pd.read_csv(file_path)

# Check if the file has data
if df.empty or len(df) < 1:
    print("The train.csv file is empty. Add some data to see the AI work!")
    exit()

# 3. Prepare data (X = Time, y = Cost)
df['month_index'] = np.arange(len(df))
X = df[['month_index']]
y = df['cost']

# 4. Train the Model
model = LinearRegression()
model.fit(X, y)

# 5. Predict next month
next_month = np.array([[len(df)]])
prediction = model.predict(next_month)[0]

print(f"\n--- AWS Cost AI Predictor ---")
print(f"Historical Data Points: {len(df)}")
print(f"Latest Month Cost: ${df['cost'].iloc[-1]:.2f}")
print(f"AI Predicted Next Month: ${max(0, prediction):.2f}")

if prediction > df['cost'].iloc[-1]:
    print("📈 Trend: Increasing. Recommendation: Review active EC2 instances.")
else:
    print("📉 Trend: Stable or Decreasing. Good job!")