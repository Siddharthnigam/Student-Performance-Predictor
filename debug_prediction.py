import sys
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')

from predictor.ml_core.prediction_logic import StudentScorePredictor

# Test with different scenarios
test_cases = [
    {
        'name': 'Low performer',
        'data': {
            'state': 'Bihar',
            'school_type': 'Government',
            'medium_of_instruction': 'Regional',
            'internet_access': False,
            'study_hours_per_day': 1.0,
            'tuition_classes': False,
            'attendance_rate': 50.0,
            'test_preparation': 'None',
            'previous_exam_score': 30.0,
            'board_type': 'State Board'
        }
    },
    {
        'name': 'Average performer',
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
        }
    },
    {
        'name': 'High performer',
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
    }
]

predictor = StudentScorePredictor()

for test in test_cases:
    result = predictor.predict(test['data'])
    print(f"{test['name']}: {result:.2f}")
    
    # Debug calculation
    data = test['data']
    base_score = 50
    school_score = predictor.school_type_scores.get(data['school_type'], 0)
    medium_score = predictor.medium_scores.get(data['medium_of_instruction'], 0)
    internet_score = 3 if data['internet_access'] else 0
    study_score = data['study_hours_per_day'] * 2.5
    tuition_score = 5 if data['tuition_classes'] else 0
    attendance_score = data['attendance_rate'] * 0.1
    prep_score = predictor.prep_scores.get(data['test_preparation'], 0)
    previous_score_contrib = data['previous_exam_score'] * 0.2
    board_score = predictor.board_scores.get(data['board_type'], 0)
    
    predicted_score = (base_score + school_score + medium_score + 
                      internet_score + study_score + tuition_score + 
                      attendance_score + prep_score + previous_score_contrib + 
                      board_score)
    
    state_multiplier = predictor.state_multipliers.get(data['state'], 1.0)
    final_score = predicted_score * state_multiplier
    
    print(f"  Debug: base={base_score}, school={school_score}, medium={medium_score}")
    print(f"  internet={internet_score}, study={study_score}, tuition={tuition_score}")
    print(f"  attendance={attendance_score}, prep={prep_score}, previous={previous_score_contrib}, board={board_score}")
    print(f"  predicted={predicted_score}, multiplier={state_multiplier}, final={final_score}")
    print()