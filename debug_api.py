import requests
import json

# Test what the API actually expects
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

try:
    response = requests.post('http://127.0.0.1:8000/api/predict/', json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Also test with old field names to see if that's what it wants
old_test_data = {
    'attendance': 75.0,
    'assignment_scores': 78.0,
    'quiz_scores': 82.0
}

try:
    response = requests.post('http://127.0.0.1:8000/api/predict/', json=old_test_data)
    print(f"Old fields Status: {response.status_code}")
    print(f"Old fields Response: {response.text}")
except Exception as e:
    print(f"Old fields Error: {e}")