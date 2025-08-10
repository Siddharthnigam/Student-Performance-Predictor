# Student Performance Prediction API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoints

### 1. Health Check
**GET** `/health/`

Check if the API and ML model are working.

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Model Information
**GET** `/model/info/`

Get information about the ML model and supported features.

**Response:**
```json
{
  "success": true,
  "model_type": "decision_tree",
  "training_metrics": {
    "mae": 5.97,
    "rmse": 7.37,
    "r2_score": 0.569
  },
  "supported_features": [...],
  "valid_values": {...}
}
```

### 3. Single Prediction
**POST** `/predict/`

Predict performance for a single student.

**Request Body:**
```json
{
  "state": "Maharashtra",
  "school_type": "private",
  "medium_of_instruction": "English",
  "internet_access": true,
  "study_hours_per_day": 6.0,
  "tuition_classes": true,
  "attendance_rate": 90.0,
  "test_preparation": "coaching",
  "previous_exam_score": 85.0,
  "board_type": "CBSE"
}
```

**Response:**
```json
{
  "success": true,
  "predicted_score": 89.32,
  "performance_category": "[EXCELLENT] Excellent (80-89)",
  "confidence_level": "[HIGH] High (90%+ data completeness)",
  "key_factors": [...],
  "recommendations": [...]
}
```

### 4. Batch Prediction
**POST** `/predict/batch/`

Predict performance for multiple students.

**Request Body:**
```json
{
  "students": [
    {
      "state": "Maharashtra",
      "school_type": "private",
      ...
    },
    {
      "state": "Bihar",
      "school_type": "government",
      ...
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "index": 0,
      "predicted_score": 89.32,
      "performance_category": "[EXCELLENT] Excellent (80-89)"
    },
    {
      "index": 1,
      "predicted_score": 47.01,
      "performance_category": "[REQUIRES ATTENTION] Requires Attention (<50)"
    }
  ],
  "total_processed": 2
}
```

## Feature Requirements

### Required Fields
- `state`: String (MP, Maharashtra, Tamil Nadu, etc.)
- `school_type`: String (government, private, aided)
- `medium_of_instruction`: String (Hindi, English, regional)
- `internet_access`: Boolean
- `study_hours_per_day`: Float (0-24)
- `tuition_classes`: Boolean
- `attendance_rate`: Float (0-100)
- `test_preparation`: String (none, self-study, coaching)
- `previous_exam_score`: Float (0-100)
- `board_type`: String (CBSE, ICSE, State Board, IB, NIOS)

## Error Responses

```json
{
  "success": false,
  "error": "Error message description"
}
```

## Usage Examples

### JavaScript/Frontend
```javascript
// Single prediction
const response = await fetch('http://127.0.0.1:8000/api/predict/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    state: 'Maharashtra',
    school_type: 'private',
    // ... other fields
  })
});

const data = await response.json();
console.log('Predicted Score:', data.predicted_score);
```

### Python
```python
import requests

response = requests.post('http://127.0.0.1:8000/api/predict/', json={
    'state': 'Maharashtra',
    'school_type': 'private',
    # ... other fields
})

data = response.json()
print(f"Predicted Score: {data['predicted_score']}/100")
```