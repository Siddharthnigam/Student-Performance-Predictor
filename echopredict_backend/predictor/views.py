from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentDataSerializer
from .prediction_service import predict_student_score

class PredictScoreView(APIView):
    def post(self, request):
        serializer = StudentDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                prediction = predict_student_score(serializer.validated_data)
                return Response({'prediction': prediction}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModelStatusView(APIView):
    def get(self, request):
        try:
            from .ml_core.prediction_logic import StudentScorePredictor
            StudentScorePredictor()
            return Response({'status': 'Prediction system is ready'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'System not available', 'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)