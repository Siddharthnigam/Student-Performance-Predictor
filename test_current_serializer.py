import sys
import os
import django

# Setup Django
sys.path.append('c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'echopredict_backend.settings')
django.setup()

from predictor.serializers import StudentDataSerializer

# Test with frontend data format
frontend_data = {
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

print("Testing current serializer...")
serializer = StudentDataSerializer(data=frontend_data)
print(f"Is valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    print("Validation successful!")
    print(f"Validated data: {serializer.validated_data}")