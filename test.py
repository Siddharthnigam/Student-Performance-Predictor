import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load the dataset (replace with actual path)
df = pd.read_csv("student_scores.csv")

# Example feature setup
X = df[["math_score", "reading_score"]]
y = df["writing_score"]  # Or whatever you're predicting

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, "echopredict_backend/predictor/ml_model/student_model.joblib")

print("✅ Model saved successfully")