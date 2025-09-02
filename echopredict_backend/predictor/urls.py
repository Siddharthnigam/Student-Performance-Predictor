from django.urls import path
from .views import PredictScoreView, ModelStatusView

urlpatterns = [
    path('predict/', PredictScoreView.as_view(), name='predict-score'),
    path('status/', ModelStatusView.as_view(), name='model-status'),
]