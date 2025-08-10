# Student Performance Prediction System

A complete ML system to predict student performance in the Indian education context.

## 🚀 Quick Start

1. **Start Backend:**
   ```bash
   python manage.py runserver 8000
   ```

2. **Start Frontend:**
   ```bash
   cd ../frontend
   npm run dev
   ```

3. **Open:** http://localhost:5173

## 📁 Structure

```
student_predictor/
├── api/                    # REST API endpoints
├── ml_core/               # Machine Learning system
├── student_predictor/     # Django configuration
├── docs/                  # All documentation
├── manage.py             # Django management
├── requirements.txt      # Dependencies
└── test_api.py          # API tests
```

## 🎯 Features

- **10 Input Features** for Indian education context
- **Real-time Predictions** via REST API
- **Detailed Explanations** with recommendations
- **React Frontend** with Tailwind CSS
- **CORS Enabled** for frontend integration

## 📊 API Endpoints

- `GET /api/health/` - Health check
- `POST /api/predict/` - Single prediction
- `POST /api/predict/batch/` - Batch predictions
- `GET /api/model/info/` - Model information

See `docs/` folder for complete documentation.