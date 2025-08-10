"""
Prediction Module for Student Performance Prediction

This module handles:
- Loading trained model and feature engineer
- Making predictions on new student data
- Providing detailed explanations for predictions
- Handling input validation and preprocessing

Author: Student Performance ML System
"""

import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Union, Tuple

class StudentPerformancePredictor:
    """
    Student Performance Predictor Class
    
    Loads trained model and provides prediction functionality with explanations
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the predictor by loading the trained model
        
        Args:
            model_path (str, optional): Path to the saved model file
        """
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'student_model.joblib')
        
        try:
            # Load the saved model data
            self.model_data = joblib.load(model_path)
            self.model = self.model_data['model']
            self.feature_engineer = self.model_data['feature_engineer']
            self.model_type = self.model_data.get('model_type', 'unknown')
            self.training_metrics = self.model_data.get('training_metrics', {})
            
            print(f"[SUCCESS] Model loaded successfully!")
            print(f"   Model type: {self.model_type.replace('_', ' ').title()}")
            if self.training_metrics:
                print(f"   Training MAE: {self.training_metrics.get('mae', 'N/A'):.2f}")
                print(f"   Training R2: {self.training_metrics.get('r2_score', 'N/A'):.3f}")
            
        except FileNotFoundError:
            raise FileNotFoundError(
                f"[ERROR] Model file not found at {model_path}. "
                "Please run train_model.py first to train the model."
            )
        except Exception as e:
            raise Exception(f"[ERROR] Error loading model: {str(e)}")
    
    def validate_input(self, student_data: Dict) -> Dict:
        """
        Validate and clean input data
        
        Args:
            student_data (dict): Raw student data dictionary
            
        Returns:
            dict: Validated and cleaned student data
        """
        # Define expected features and their types/ranges
        expected_features = {
            'state': str,
            'school_type': str,
            'medium_of_instruction': str,
            'internet_access': bool,
            'study_hours_per_day': (int, float),
            'tuition_classes': bool,
            'attendance_rate': (int, float),
            'test_preparation': str,
            'previous_exam_score': (int, float),
            'board_type': str
        }
        
        # Valid values for categorical features
        valid_values = {
            'state': ['MP', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'UP', 'Bihar', 
                     'West Bengal', 'Gujarat', 'Kerala', 'Rajasthan', 'Punjab', 'Haryana'],
            'school_type': ['government', 'private', 'aided'],
            'medium_of_instruction': ['Hindi', 'English', 'regional'],
            'test_preparation': ['none', 'self-study', 'coaching'],
            'board_type': ['CBSE', 'ICSE', 'State Board', 'IB', 'NIOS']
        }
        
        validated_data = {}
        
        # Validate each feature
        for feature, expected_type in expected_features.items():
            if feature in student_data:
                value = student_data[feature]
                
                # Type validation
                if not isinstance(value, expected_type):
                    if feature in ['study_hours_per_day', 'attendance_rate', 'previous_exam_score']:
                        try:
                            value = float(value)
                        except (ValueError, TypeError):
                            raise ValueError(f"[ERROR] {feature} must be a number")
                    elif feature in ['internet_access', 'tuition_classes']:
                        if isinstance(value, str):
                            value = value.lower() in ['true', '1', 'yes', 'on']
                        else:
                            value = bool(value)
                
                # Range validation for numerical features
                if feature == 'study_hours_per_day' and not (0 <= value <= 24):
                    raise ValueError("[ERROR] study_hours_per_day must be between 0 and 24")
                elif feature == 'attendance_rate' and not (0 <= value <= 100):
                    raise ValueError("[ERROR] attendance_rate must be between 0 and 100")
                elif feature == 'previous_exam_score' and not (0 <= value <= 100):
                    raise ValueError("[ERROR] previous_exam_score must be between 0 and 100")
                
                # Categorical value validation
                if feature in valid_values and value not in valid_values[feature]:
                    print(f"[WARNING] '{value}' is not a standard value for {feature}")
                    print(f"   Valid values: {valid_values[feature]}")
                
                validated_data[feature] = value
            else:
                # Feature is missing - will be handled by feature engineer
                print(f"[WARNING] Missing feature '{feature}' - will use default value")
        
        return validated_data
    
    def predict(self, student_data: Dict, explain: bool = True) -> Union[float, Tuple[float, Dict]]:
        """
        Predict student performance score
        
        Args:
            student_data (dict): Dictionary containing student features
            explain (bool): Whether to return explanation along with prediction
            
        Returns:
            float or tuple: Predicted score, optionally with explanation
        """
        try:
            # Validate input data
            validated_data = self.validate_input(student_data)
            
            # Convert to DataFrame for processing
            df = pd.DataFrame([validated_data])
            
            # Apply feature engineering (same as training)
            processed_df = self.feature_engineer.transform(df)
            
            # Make prediction
            raw_prediction = self.model.predict(processed_df)[0]
            
            # Apply business rules and constraints
            final_prediction = self._apply_business_rules(raw_prediction, validated_data)
            
            if explain:
                explanation = self._generate_explanation(validated_data, final_prediction)
                return final_prediction, explanation
            else:
                return final_prediction
                
        except Exception as e:
            raise Exception(f"[ERROR] Prediction error: {str(e)}")
    
    def _apply_business_rules(self, prediction: float, student_data: Dict) -> float:
        """
        Apply business rules and constraints to the raw prediction
        
        Args:
            prediction (float): Raw model prediction
            student_data (dict): Original student data
            
        Returns:
            float: Adjusted prediction
        """
        # Cap prediction between 0 and 100
        adjusted_prediction = np.clip(prediction, 0, 100)
        
        # Apply additional business logic if needed
        # For example, if attendance is very low, cap the maximum possible score
        if student_data.get('attendance_rate', 100) < 50:
            adjusted_prediction = min(adjusted_prediction, 75)
        
        # If no previous exam score and no tuition, be more conservative
        if (student_data.get('previous_exam_score', 100) < 40 and 
            not student_data.get('tuition_classes', True)):
            adjusted_prediction = min(adjusted_prediction, 70)
        
        return round(adjusted_prediction, 2)
    
    def _generate_explanation(self, student_data: Dict, prediction: float) -> Dict:
        """
        Generate detailed explanation for the prediction
        
        Args:
            student_data (dict): Student input data
            prediction (float): Final prediction
            
        Returns:
            dict: Detailed explanation of the prediction
        """
        explanation = {
            'predicted_score': prediction,
            'performance_category': self._get_performance_category(prediction),
            'key_factors': [],
            'recommendations': [],
            'confidence_level': self._get_confidence_level(student_data)
        }
        
        # Analyze key factors affecting the prediction
        factors = []
        
        # Previous exam score impact
        prev_score = student_data.get('previous_exam_score', 75)
        if prev_score >= 85:
            factors.append("[STRONG] Strong previous performance indicates consistent academic ability")
        elif prev_score >= 70:
            factors.append("[GOOD] Good previous performance provides solid foundation")
        elif prev_score >= 50:
            factors.append("[AVERAGE] Average previous performance suggests room for improvement")
        else:
            factors.append("[LOW] Low previous performance indicates need for significant improvement")
        
        # Study hours impact
        study_hours = student_data.get('study_hours_per_day', 4)
        if study_hours >= 6:
            factors.append("[HIGH STUDY] High study hours (6+ hrs/day) strongly support good performance")
        elif study_hours >= 4:
            factors.append("[MODERATE STUDY] Moderate study hours (4-6 hrs/day) provide decent preparation")
        else:
            factors.append("[LOW STUDY] Low study hours (<4 hrs/day) may limit performance potential")
        
        # Attendance impact
        attendance = student_data.get('attendance_rate', 85)
        if attendance >= 90:
            factors.append("[EXCELLENT ATTENDANCE] Excellent attendance (90%+) ensures consistent learning")
        elif attendance >= 75:
            factors.append("[GOOD ATTENDANCE] Good attendance (75-90%) supports regular learning")
        else:
            factors.append("[POOR ATTENDANCE] Poor attendance (<75%) significantly impacts learning")
        
        # Tuition classes impact
        if student_data.get('tuition_classes', False):
            factors.append("[TUITION] Tuition classes provide additional academic support")
        else:
            factors.append("[SELF-STUDY] Self-study approach requires strong discipline")
        
        # Internet access impact
        if student_data.get('internet_access', False):
            factors.append("[INTERNET] Internet access enables modern learning resources")
        else:
            factors.append("[TRADITIONAL] Limited to traditional learning resources")
        
        # Board type impact
        board = student_data.get('board_type', 'State Board')
        if board == 'IB':
            factors.append("[IB BOARD] IB curriculum known for rigorous academic standards")
        elif board == 'ICSE':
            factors.append("[ICSE BOARD] ICSE board emphasizes comprehensive education")
        elif board == 'CBSE':
            factors.append("[CBSE BOARD] CBSE board provides standardized national curriculum")
        
        explanation['key_factors'] = factors
        
        # Generate recommendations
        recommendations = []
        
        if study_hours < 4:
            recommendations.append("[STUDY MORE] Increase daily study hours to at least 4-5 hours")
        
        if attendance < 80:
            recommendations.append("[ATTEND MORE] Improve attendance to above 80% for better learning")
        
        if not student_data.get('tuition_classes', False) and prev_score < 60:
            recommendations.append("[TUITION] Consider joining tuition classes for additional support")
        
        if not student_data.get('internet_access', False):
            recommendations.append("[INTERNET] Access to internet can provide valuable learning resources")
        
        if student_data.get('test_preparation', 'none') == 'none':
            recommendations.append("[TEST PREP] Structured test preparation can significantly improve scores")
        
        if prediction < 60:
            recommendations.append("[FUNDAMENTALS] Focus on strengthening fundamental concepts")
            recommendations.append("[HELP] Seek help from teachers or peers for difficult topics")
        
        explanation['recommendations'] = recommendations
        
        return explanation
    
    def _get_performance_category(self, score: float) -> str:
        """Get performance category based on score"""
        if score >= 90:
            return "[OUTSTANDING] Outstanding (90-100)"
        elif score >= 80:
            return "[EXCELLENT] Excellent (80-89)"
        elif score >= 70:
            return "[GOOD] Good (70-79)"
        elif score >= 60:
            return "[SATISFACTORY] Satisfactory (60-69)"
        elif score >= 50:
            return "[NEEDS IMPROVEMENT] Needs Improvement (50-59)"
        else:
            return "[REQUIRES ATTENTION] Requires Attention (<50)"
    
    def _get_confidence_level(self, student_data: Dict) -> str:
        """Determine confidence level based on data completeness and quality"""
        missing_features = 0
        total_features = 10
        
        expected_features = [
            'state', 'school_type', 'medium_of_instruction', 'internet_access',
            'study_hours_per_day', 'tuition_classes', 'attendance_rate',
            'test_preparation', 'previous_exam_score', 'board_type'
        ]
        
        for feature in expected_features:
            if feature not in student_data:
                missing_features += 1
        
        completeness = (total_features - missing_features) / total_features
        
        if completeness >= 0.9:
            return "[HIGH] High (90%+ data completeness)"
        elif completeness >= 0.7:
            return "[MEDIUM] Medium (70-90% data completeness)"
        else:
            return "[LOW] Low (<70% data completeness)"

def predict_student_performance(student_data: Dict, explain: bool = True):
    """
    Convenience function to make predictions
    
    Args:
        student_data (dict): Student data dictionary
        explain (bool): Whether to return explanation
        
    Returns:
        Prediction result with optional explanation
    """
    predictor = StudentPerformancePredictor()
    return predictor.predict(student_data, explain)

def main():
    """
    Main function demonstrating prediction functionality
    """
    print("[SYSTEM] Student Performance Prediction System")
    print("=" * 50)
    
    # Sample student data for demonstration
    sample_students = [
        {
            'state': 'Maharashtra',
            'school_type': 'private',
            'medium_of_instruction': 'English',
            'internet_access': True,
            'study_hours_per_day': 6.0,
            'tuition_classes': True,
            'attendance_rate': 92.0,
            'test_preparation': 'coaching',
            'previous_exam_score': 85.0,
            'board_type': 'CBSE'
        },
        {
            'state': 'Bihar',
            'school_type': 'government',
            'medium_of_instruction': 'Hindi',
            'internet_access': False,
            'study_hours_per_day': 3.5,
            'tuition_classes': False,
            'attendance_rate': 78.0,
            'test_preparation': 'self-study',
            'previous_exam_score': 65.0,
            'board_type': 'State Board'
        }
    ]
    
    try:
        predictor = StudentPerformancePredictor()
        
        for i, student in enumerate(sample_students, 1):
            print(f"\n[PREDICTION] Sample Prediction {i}:")
            print("-" * 30)
            
            # Make prediction with explanation
            score, explanation = predictor.predict(student, explain=True)
            
            print(f"[SCORE] Predicted Score: {score}/100")
            print(f"[CATEGORY] Category: {explanation['performance_category']}")
            print(f"[CONFIDENCE] Confidence: {explanation['confidence_level']}")
            
            print(f"\n[FACTORS] Key Factors:")
            for factor in explanation['key_factors'][:3]:  # Show top 3 factors
                print(f"   • {factor}")
            
            if explanation['recommendations']:
                print(f"\n[RECOMMENDATIONS] Recommendations:")
                for rec in explanation['recommendations'][:2]:  # Show top 2 recommendations
                    print(f"   • {rec}")
            
            print("-" * 50)
    
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        print("[INFO] Make sure to run train_model.py first to train the model.")

if __name__ == "__main__":
    main()