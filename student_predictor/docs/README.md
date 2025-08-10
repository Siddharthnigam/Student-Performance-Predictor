# 🎓 Student Performance Prediction System

A comprehensive machine learning system designed to predict student performance scores (0-100) based on culturally relevant inputs from the Indian education context.

## 📋 Overview

This system uses supervised machine learning to predict student final exam scores based on various educational and socio-economic factors specific to the Indian education system. The model considers state-wise variations, different board types, and cultural factors that influence student performance.

## 🎯 Features

### Input Features
- **State**: Indian states (MP, Maharashtra, Tamil Nadu, etc.)
- **School Type**: Government, Private, Aided
- **Medium of Instruction**: Hindi, English, Regional languages
- **Internet Access**: Boolean (availability of internet)
- **Study Hours per Day**: Float (daily study time)
- **Tuition Classes**: Boolean (external coaching)
- **Attendance Rate**: Percentage (0-100)
- **Test Preparation**: None, Self-study, Coaching
- **Previous Exam Score**: Float (0-100)
- **Board Type**: CBSE, ICSE, State Board, IB, NIOS

### Target Variable
- **Final Score**: Float (0-100) - Predicted exam performance

## 🏗️ System Architecture

### Modular Structure
```
mlcore/
├── feature_engineering.py    # Data preprocessing and encoding
├── train_model.py           # Model training and evaluation
├── predictor.py             # Prediction engine with explanations
├── demo.py                  # Interactive demonstration
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

### Key Components

1. **Feature Engineering** (`feature_engineering.py`)
   - One-Hot Encoding for categorical features
   - StandardScaler for numerical features
   - Missing value imputation with contextual defaults
   - Boolean feature conversion

2. **Model Training** (`train_model.py`)
   - Synthetic data generation with Indian education context
   - Decision Tree Regressor with optimized parameters
   - Comprehensive evaluation metrics (MAE, RMSE, R²)
   - Model persistence using joblib

3. **Prediction Engine** (`predictor.py`)
   - Input validation and preprocessing
   - Business rule application
   - Detailed prediction explanations
   - Confidence level assessment

4. **Demo System** (`demo.py`)
   - Complete workflow demonstration
   - Interactive prediction mode
   - Multiple test case scenarios

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```python
python train_model.py
```

### 3. Make Predictions
```python
from predictor import predict_student_performance

# Sample student data
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

# Get prediction with explanation
score, explanation = predict_student_performance(student_data, explain=True)
print(f"Predicted Score: {score}/100")
```

### 4. Run Interactive Demo
```python
python demo.py
```

## 📊 Model Performance

The system achieves the following performance metrics on synthetic test data:

- **Mean Absolute Error (MAE)**: ~5-8 points
- **Root Mean Square Error (RMSE)**: ~7-10 points  
- **R² Score**: ~0.75-0.85 (75-85% variance explained)

## 🎯 Key Features

### 1. Cultural Context Integration
- **State-based Multipliers**: Reflects regional education quality variations
- **Board-specific Adjustments**: Different scoring patterns for CBSE, ICSE, State Boards, etc.
- **Medium of Instruction Impact**: Considers language barriers and advantages

### 2. Intelligent Preprocessing
- **Contextual Missing Value Handling**: Uses education-specific defaults
- **Feature Encoding**: Proper handling of categorical variables
- **Scaling**: Normalized numerical features for optimal model performance

### 3. Business Logic Integration
- **Score Capping**: Ensures predictions stay within 0-100 range
- **Attendance-based Constraints**: Low attendance caps maximum possible scores
- **Performance Consistency Checks**: Validates predictions against input patterns

### 4. Comprehensive Explanations
- **Performance Categories**: Outstanding, Excellent, Good, Satisfactory, etc.
- **Key Factor Analysis**: Identifies primary drivers of the prediction
- **Actionable Recommendations**: Specific suggestions for improvement
- **Confidence Levels**: Based on data completeness and quality

## 🔧 Advanced Usage

### Custom Model Training
```python
from train_model import train_model

# Train with Linear Regression instead of Decision Tree
model, feature_engineer = train_model('linear_regression')
```

### Batch Predictions
```python
from predictor import StudentPerformancePredictor
import pandas as pd

predictor = StudentPerformancePredictor()

# Load multiple students data
students_df = pd.read_csv('students.csv')

# Make batch predictions
predictions = []
for _, student in students_df.iterrows():
    score = predictor.predict(student.to_dict(), explain=False)
    predictions.append(score)
```

### Model Evaluation
```python
from sklearn.metrics import mean_absolute_error, r2_score

# Evaluate on new test data
y_true = [85, 72, 91, 68, 79]  # Actual scores
y_pred = [83, 74, 89, 65, 81]  # Predicted scores

mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"MAE: {mae:.2f}, R²: {r2:.3f}")
```

## 📈 Sample Predictions

### High Performer (Urban Private School)
```
Input: Maharashtra, Private, English, Internet=Yes, 7hrs study, Tuition=Yes, 95% attendance
Prediction: 89.5/100 (Excellent Performance)
Key Factors: Strong previous performance, High study hours, Excellent attendance
```

### Average Performer (Government School)
```
Input: MP, Government, Hindi, Internet=Yes, 4.5hrs study, Tuition=Yes, 82% attendance  
Prediction: 74.2/100 (Good Performance)
Key Factors: Moderate study hours, Good attendance, Tuition support
```

### Struggling Student (Rural Area)
```
Input: Bihar, Government, Hindi, Internet=No, 3hrs study, Tuition=No, 68% attendance
Prediction: 52.8/100 (Needs Improvement)
Recommendations: Increase study hours, Improve attendance, Consider tuition classes
```

## 🛠️ Technical Details

### Machine Learning Pipeline
1. **Data Generation**: Synthetic data with realistic correlations
2. **Preprocessing**: Feature encoding and scaling
3. **Model Training**: Decision Tree Regressor with hyperparameter tuning
4. **Evaluation**: Multiple metrics for comprehensive assessment
5. **Prediction**: Real-time scoring with explanations

### Feature Engineering Process
1. **Categorical Encoding**: One-Hot Encoding for nominal features
2. **Numerical Scaling**: StandardScaler for continuous variables
3. **Missing Value Imputation**: Context-aware default values
4. **Feature Validation**: Input range and type checking

### Model Architecture
- **Algorithm**: Decision Tree Regressor
- **Max Depth**: 10 (prevents overfitting)
- **Min Samples Split**: 20
- **Min Samples Leaf**: 10
- **Random State**: 42 (reproducibility)

## 🔍 Validation and Testing

### Input Validation
- Type checking for all features
- Range validation for numerical inputs
- Categorical value verification
- Missing value handling

### Model Validation
- Train-test split (80-20)
- Cross-validation ready architecture
- Performance metric tracking
- Prediction consistency checks

## 📚 Dependencies

### Core Libraries
- `scikit-learn>=1.3.0` - Machine learning algorithms
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computations
- `joblib>=1.3.0` - Model persistence

### Optional Libraries
- `matplotlib>=3.7.0` - Visualization
- `seaborn>=0.12.0` - Statistical plots
- `jupyter>=1.0.0` - Interactive development

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Indian education system research and statistics
- Scikit-learn community for excellent ML tools
- Open source contributors and educators

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team
- Check documentation and examples

---

**Built with ❤️ for Indian Education System**