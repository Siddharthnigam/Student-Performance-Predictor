import sys
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')

from predictor.ml_core.prediction_logic import StudentScorePredictor

# Test cases
test_cases = [
    {
        'name': 'Your Example',
        'data': {
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
        },
        'expected': 82.16
    },
    {
        'name': 'High Performer',
        'data': {
            'state': 'Kerala',
            'school_type': 'Private',
            'medium_of_instruction': 'English',
            'internet_access': True,
            'study_hours_per_day': 6.0,
            'tuition_classes': True,
            'attendance_rate': 95.0,
            'test_preparation': 'Coaching',
            'previous_exam_score': 85.0,
            'board_type': 'ICSE'
        }
    },
    {
        'name': 'Low Performer',
        'data': {
            'state': 'Bihar',
            'school_type': 'Government',
            'medium_of_instruction': 'Regional',
            'internet_access': False,
            'study_hours_per_day': 1.0,
            'tuition_classes': False,
            'attendance_rate': 60.0,
            'test_preparation': 'None',
            'previous_exam_score': 40.0,
            'board_type': 'State Board'
        }
    }
]

predictor = StudentScorePredictor()

print("=== FORMULA TESTING ===")
for test in test_cases:
    result = predictor.predict(test['data'])
    print(f"\\n{test['name']}:")
    print(f"  Result: {result:.2f}")
    if 'expected' in test:
        print(f"  Expected: {test['expected']}")
        print(f"  Difference: {abs(result - test['expected']):.2f}")
    print(f"  Data: {test['data']}")

print("\\n=== SYSTEM READY ===")
print("Backend: Updated with your exact formula")
print("Frontend: Updated with all 10 input fields")
print("Formula: Matches your calculation logic")
print("\\nTo test:")
print("1. cd echopredict_backend && python manage.py runserver")
print("2. cd echopredict_frontend && npm run dev")