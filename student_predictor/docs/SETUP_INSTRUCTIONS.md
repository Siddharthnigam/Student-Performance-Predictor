# Setup Instructions for Student Performance Prediction API

## Current Status
The backend is structured and API endpoints are created. However, ML dependencies need to be installed in the virtual environment.

## Quick Setup Steps

### 1. Install ML Dependencies in Virtual Environment
```bash
# Navigate to the project root
cd C:\Users\siddh\OneDrive\Desktop\splitz

# Activate virtual environment
env\Scripts\activate

# Install ML packages
pip install pandas numpy scikit-learn joblib

# Navigate to backend
cd student_predictor
```

### 2. Train the ML Model
```bash
# Train the model (from student_predictor directory)
python ml_core/train_model.py
```

### 3. Update API to Use Full ML System
```bash
# Edit api/urls.py - change back to:
from . import views  # instead of views_simple

# Add back all endpoints in urls.py
```

### 4. Start Server
```bash
python manage.py runserver 8000
```

## Current Working Endpoints (Simple Version)

- `GET /api/health/` - Health check
- `POST /api/predict/` - Mock prediction

## Test the API
```bash
python test_api_simple.py
```

## Frontend Integration Example
```javascript
// Test the mock API
fetch('http://127.0.0.1:8000/api/predict/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    state: 'Maharashtra',
    school_type: 'private',
    previous_exam_score: 85.0
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Next Steps
1. Install ML dependencies in virtual environment
2. Train the model
3. Switch back to full ML API
4. Test all endpoints
5. Integrate with frontend