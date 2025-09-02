import sys
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')

# Manual calculation based on your example
base_score = 50
school_type_score = -5  # Government
medium_score = 0  # Hindi
internet_score = 0  # No
study_score = 2.5 * 2.5  # 6.25
tuition_score = 0  # No
attendance_score = 75 * 0.1  # 7.5
prep_score = 3  # Self-study
previous_score_contrib = 60 * 0.2  # 12
board_score = 5  # CBSE

predicted_score = (base_score + school_type_score + medium_score + 
                  internet_score + study_score + tuition_score + 
                  attendance_score + prep_score + previous_score_contrib + 
                  board_score)

print("Manual Calculation:")
print(f"base_score: {base_score}")
print(f"school_type_score: {school_type_score}")
print(f"medium_score: {medium_score}")
print(f"internet_score: {internet_score}")
print(f"study_score: {study_score}")
print(f"tuition_score: {tuition_score}")
print(f"attendance_score: {attendance_score}")
print(f"prep_score: {prep_score}")
print(f"previous_score_contrib: {previous_score_contrib}")
print(f"board_score: {board_score}")
print(f"predicted_score: {predicted_score}")

state_multiplier = 1.05  # Maharashtra
final_score = predicted_score * state_multiplier
print(f"final_score: {final_score}")

# Test with code
from predictor.ml_core.prediction_logic import StudentScorePredictor

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
code_result = predictor.predict(test_data)
print(f"Code result: {code_result}")
print(f"Expected: 82.16")
print(f"Difference: {abs(code_result - 82.16)}")