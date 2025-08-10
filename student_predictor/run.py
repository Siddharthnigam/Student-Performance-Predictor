"""
Simple server runner for Student Performance Prediction System
"""

import subprocess
import sys
import os

def main():
    print("🎓 Student Performance Prediction System")
    print("=" * 50)
    print("Starting Django server on http://127.0.0.1:8000")
    print("API endpoints available at /api/")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()