"""
API Tests for Student Performance Prediction System
"""

import json
import requests
import sys
import os

# Add ml_core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_core'))

BASE_URL = "http://127.0.0.1:8000/api"

def test_health_check():
    """Test health check endpoint"""
    print("[TEST] Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n[TEST] Model Info")
    try:
        response = requests.get(f"{BASE_URL}/model/info/")
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Model Type: {data.get('model_type')}")
        print(f"Features: {len(data.get('supported_features', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n[TEST] Single Prediction")
    
    student_data = {
        'state': 'Maharashtra',
        'school_type': 'private',
        'medium_of_instruction': 'English',
        'internet_access': True,
        'study_hours_per_day': 6.0,
        'tuition_classes': True,
        'attendance_rate': 90.0,
        'test_preparation': 'coaching',
        'previous_exam_score': 85.0,
        'board_type': 'CBSE'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict/",
            json=student_data,
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Predicted Score: {data.get('predicted_score')}/100")
        print(f"Category: {data.get('performance_category')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n[TEST] Batch Prediction")
    
    batch_data = {
        'students': [
            {
                'state': 'Maharashtra',
                'school_type': 'private',
                'medium_of_instruction': 'English',
                'internet_access': True,
                'study_hours_per_day': 6.0,
                'tuition_classes': True,
                'attendance_rate': 90.0,
                'test_preparation': 'coaching',
                'previous_exam_score': 85.0,
                'board_type': 'CBSE'
            },
            {
                'state': 'Bihar',
                'school_type': 'government',
                'medium_of_instruction': 'Hindi',
                'internet_access': False,
                'study_hours_per_day': 3.0,
                'tuition_classes': False,
                'attendance_rate': 70.0,
                'test_preparation': 'none',
                'previous_exam_score': 55.0,
                'board_type': 'State Board'
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch/",
            json=batch_data,
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Total Processed: {data.get('total_processed')}")
        for result in data.get('results', []):
            print(f"Student {result['index']}: {result.get('predicted_score', 'Error')}/100")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("API Testing for Student Performance Prediction")
    print("=" * 50)
    print("Make sure Django server is running on port 8000")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_model_info,
        test_single_prediction,
        test_batch_prediction
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n[SUMMARY] {passed}/{len(tests)} tests passed")

if __name__ == "__main__":
    main()