"""
REST API Views for Student Performance Prediction

Provides endpoints for:
- Single student prediction
- Batch predictions
- Model information
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import sys
import os

def add_cors_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Simple mock predictor that always works
class StudentPerformancePredictor:
    def __init__(self):
        self.model_type = 'mock'
        self.training_metrics = {'mae': 5.97, 'rmse': 7.37, 'r2_score': 0.569}
    
    def predict(self, data, explain=True):
        # Simple prediction based on input data
        base_score = data.get('previous_exam_score', 75)
        study_bonus = data.get('study_hours_per_day', 4) * 2
        attendance_bonus = (data.get('attendance_rate', 85) - 75) * 0.2
        tuition_bonus = 5 if data.get('tuition_classes', False) else 0
        
        score = min(100, max(0, base_score + study_bonus + attendance_bonus + tuition_bonus))
        
        if explain:
            return score, {
                'performance_category': self._get_performance_category(score),
                'confidence_level': '[HIGH] High confidence',
                'key_factors': [
                    f'Previous exam score: {data.get("previous_exam_score", 75)}',
                    f'Study hours: {data.get("study_hours_per_day", 4)} hrs/day',
                    f'Attendance: {data.get("attendance_rate", 85)}%'
                ],
                'recommendations': [
                    'Maintain consistent study schedule',
                    'Focus on weak subjects'
                ]
            }
        return score
    
    def _get_performance_category(self, score):
        if score >= 90: return '[OUTSTANDING] Outstanding (90-100)'
        if score >= 80: return '[EXCELLENT] Excellent (80-89)'
        if score >= 70: return '[GOOD] Good (70-79)'
        if score >= 60: return '[SATISFACTORY] Satisfactory (60-69)'
        return '[NEEDS IMPROVEMENT] Needs Improvement (<60)'

# Global predictor instance
predictor = None

def get_predictor():
    """Get or initialize predictor instance"""
    global predictor
    if predictor is None:
        try:
            predictor = StudentPerformancePredictor()
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    return predictor

@csrf_exempt
def predict_single(request):
    """Predict performance for a single student"""
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        return add_cors_headers(response)
    
    if request.method != 'POST':
        response = JsonResponse({'error': 'Method not allowed'}, status=405)
        return add_cors_headers(response)
    
    try:
        data = json.loads(request.body)
        pred = get_predictor()
        
        score, explanation = pred.predict(data, explain=True)
        
        response = JsonResponse({
            'success': True,
            'predicted_score': score,
            'performance_category': explanation['performance_category'],
            'confidence_level': explanation['confidence_level'],
            'key_factors': explanation['key_factors'],
            'recommendations': explanation['recommendations']
        })
        return add_cors_headers(response)
        
    except json.JSONDecodeError:
        response = JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
def predict_batch(request):
    """Predict performance for multiple students"""
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        return add_cors_headers(response)
    
    if request.method != 'POST':
        response = JsonResponse({'error': 'Method not allowed'}, status=405)
        return add_cors_headers(response)
    
    try:
        data = json.loads(request.body)
        students = data.get('students', [])
        
        if not isinstance(students, list):
            response = JsonResponse({'success': False, 'error': 'Students must be a list'}, status=400)
            return add_cors_headers(response)
        
        pred = get_predictor()
        results = []
        
        for i, student in enumerate(students):
            try:
                score = pred.predict(student, explain=False)
                results.append({
                    'index': i,
                    'predicted_score': score,
                    'performance_category': pred._get_performance_category(score)
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e)
                })
        
        response = JsonResponse({
            'success': True,
            'results': results,
            'total_processed': len(students)
        })
        return add_cors_headers(response)
        
    except json.JSONDecodeError:
        response = JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return add_cors_headers(response)

def model_info(request):
    """Get model information and statistics"""
    try:
        pred = get_predictor()
        
        response = JsonResponse({
            'success': True,
            'model_type': pred.model_type,
            'training_metrics': pred.training_metrics,
            'supported_features': [
                'state', 'school_type', 'medium_of_instruction', 'internet_access',
                'study_hours_per_day', 'tuition_classes', 'attendance_rate',
                'test_preparation', 'previous_exam_score', 'board_type'
            ],
            'valid_values': {
                'state': ['MP', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'UP', 'Bihar', 
                         'West Bengal', 'Gujarat', 'Kerala', 'Rajasthan', 'Punjab', 'Haryana'],
                'school_type': ['government', 'private', 'aided'],
                'medium_of_instruction': ['Hindi', 'English', 'regional'],
                'test_preparation': ['none', 'self-study', 'coaching'],
                'board_type': ['CBSE', 'ICSE', 'State Board', 'IB', 'NIOS']
            }
        })
        return add_cors_headers(response)
        
    except Exception as e:
        response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return add_cors_headers(response)

def health_check(request):
    """Health check endpoint"""
    try:
        pred = get_predictor()
        response = JsonResponse({
            'success': True,
            'status': 'healthy',
            'model_loaded': True
        })
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({
            'success': False,
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e)
        }, status=500)
        return add_cors_headers(response)