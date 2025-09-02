import sys
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')

from predictor.serializers import StudentDataSerializer

# Test data that matches frontend
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

print("Testing serializer validation...")
serializer = StudentDataSerializer(data=test_data)
if serializer.is_valid():
    print("Serializer is valid!")
    print("Validated data:", serializer.validated_data)
    
    # Test prediction
    from predictor.ml_model.model_utils import predict_student_score
    result = predict_student_score(serializer.validated_data)
    print("Prediction result:", result)
else:
    print("Serializer errors:", serializer.errors)