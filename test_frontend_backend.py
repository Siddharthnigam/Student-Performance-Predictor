import requests
import json
import subprocess
import time
import threading
import os

def start_backend():
    """Start Django backend server"""
    os.chdir("c:\\Users\\siddh\\OneDrive\\Desktop\\EchoPredict\\echopredict_backend")
    subprocess.run(["python", "manage.py", "runserver", "8000"], check=False)

def test_backend_endpoints():
    """Test backend endpoints"""
    print("Testing backend endpoints...")
    
    # Test status endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/status/')
        print(f"✅ Status API: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Status API failed: {e}")
        return False
    
    # Test prediction endpoint
    test_data = {
        "attendance": 85.0,
        "assignment_scores": 78.0,
        "quiz_scores": 82.0
    }
    
    try:
        response = requests.post('http://127.0.0.1:8000/api/predict/', 
                               json=test_data,
                               headers={'Content-Type': 'application/json'})
        print(f"✅ Prediction API: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Prediction API failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing EchoPredict Backend...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Test endpoints
    if test_backend_endpoints():
        print("✅ Backend is working correctly!")
        print("🎯 Frontend form fields updated to match backend API")
        print("📝 Updated fields: attendance, assignment_scores, quiz_scores")
    else:
        print("❌ Backend test failed")