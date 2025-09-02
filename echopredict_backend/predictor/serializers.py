from rest_framework import serializers

class StudentDataSerializer(serializers.Serializer):
    state = serializers.CharField()
    school_type = serializers.CharField()
    medium_of_instruction = serializers.CharField()
    internet_access = serializers.BooleanField()
    study_hours_per_day = serializers.FloatField()
    tuition_classes = serializers.BooleanField()
    attendance_rate = serializers.FloatField()
    test_preparation = serializers.CharField()
    previous_exam_score = serializers.FloatField()
    board_type = serializers.CharField()