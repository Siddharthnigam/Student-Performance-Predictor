"""
API URL Configuration for Student Performance Prediction
"""

from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_single, name='predict_single'),
    path('predict/batch/', views.predict_batch, name='predict_batch'),
    path('model/info/', views.model_info, name='model_info'),
    path('health/', views.health_check, name='health_check'),
]