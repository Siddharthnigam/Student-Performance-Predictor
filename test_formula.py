import sys
import os
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')

from predictor.ml_core.prediction_logic import StudentScorePredictor

# Test with your example data
test_data = {
    'state': 'Maharashtra',
    'school_type': 'Government',
    'medium_of_instruction': 'Hindi',
    'internet_access': False,
    'study_hours_per_day': 2.5,
    'tuition_classes': False,
    'attendance_rate': 75.0,
    'test_preparation': 'Self-study',
    'previous_exam_score': 60.0,
    'board_type': 'CBSE'
}

predictor = StudentScorePredictor()
result = predictor.predict(test_data)

print("Testing Your Formula:")
print(f"Input: {test_data}")
print(f"Expected Result: 82.16")
print(f"Actual Result: {result:.2f}")
print(f"Match: {'Yes' if abs(result - 82.16) < 0.5 else 'No'}")

# Test API endpoint
import requests
try:
    response = requests.post('http://127.0.0.1:8000/api/predict/', json=test_data)
    if response.status_code == 200:
        api_result = response.json()['prediction']
        print(f"API Result: {api_result:.2f}")
    else:
        print(f"API Error: {response.status_code}")
except:
    print("API not running - start with: python manage.py runserver")