import sys
import os
import django

sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'echopredict_backend.settings')
django.setup()

from predictor.serializers import StudentDataSerializer
from predictor.prediction_service import predict_student_score

# Test data
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

print("Testing clean backend...")
serializer = StudentDataSerializer(data=test_data)
if serializer.is_valid():
    print("Serializer validation passed")
    result = predict_student_score(serializer.validated_data)
    print(f"Prediction result: {result:.2f}")
else:
    print("Serializer errors:", serializer.errors)