"""
Model Training Module for Student Performance Prediction

This module handles:
- Synthetic data generation for Indian education context
- Model training using Decision Tree Regressor
- Model evaluation with multiple metrics
- Model persistence for future predictions

Author: Student Performance ML System
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from feature_engineering import FeatureEngineer

def generate_synthetic_data(n_samples=2000):
    """
    Generate synthetic student data reflecting Indian education system
    
    Creates realistic data with proper correlations between features and target variable.
    Includes state-wise and board-wise variations common in Indian education.
    
    Args:
        n_samples (int): Number of synthetic samples to generate
        
    Returns:
        pandas.DataFrame: Generated synthetic dataset
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define realistic categories for Indian education system
    states = [
        'MP', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'UP', 'Bihar', 
        'West Bengal', 'Gujarat', 'Kerala', 'Rajasthan', 'Punjab', 'Haryana'
    ]
    
    school_types = ['government', 'private', 'aided']
    mediums = ['Hindi', 'English', 'regional']
    test_preps = ['none', 'self-study', 'coaching']
    boards = ['CBSE', 'ICSE', 'State Board', 'IB', 'NIOS']
    
    # Generate random data for each feature
    data = {
        'state': np.random.choice(states, n_samples),
        'school_type': np.random.choice(school_types, n_samples, p=[0.6, 0.3, 0.1]),  # Government schools are more common
        'medium_of_instruction': np.random.choice(mediums, n_samples, p=[0.4, 0.4, 0.2]),
        'internet_access': np.random.choice([True, False], n_samples, p=[0.65, 0.35]),  # 65% have internet
        'study_hours_per_day': np.random.normal(4.5, 1.5, n_samples).clip(1, 12),  # 1-12 hours range
        'tuition_classes': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),  # 70% take tuitions
        'attendance_rate': np.random.normal(85, 10, n_samples).clip(50, 100),  # 50-100% attendance
        'test_preparation': np.random.choice(test_preps, n_samples, p=[0.3, 0.4, 0.3]),
        'previous_exam_score': np.random.normal(75, 15, n_samples).clip(30, 100),  # Previous scores 30-100
        'board_type': np.random.choice(boards, n_samples, p=[0.4, 0.1, 0.45, 0.03, 0.02])  # State Board most common
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic target variable with meaningful correlations
    # Base score calculation considering multiple factors
    base_score = (
        df['previous_exam_score'] * 0.4 +  # Previous performance is strong predictor
        df['study_hours_per_day'] * 3 +    # More study hours = better performance
        df['attendance_rate'] * 0.2 +      # Attendance matters
        df['internet_access'].astype(int) * 5 +  # Internet access helps
        df['tuition_classes'].astype(int) * 8     # Tuition classes boost performance
    )
    
    # Apply state-based multipliers reflecting regional education quality
    state_multipliers = {
        'Kerala': 1.1,      # Known for high literacy
        'Tamil Nadu': 1.05, # Strong education system
        'Karnataka': 1.03,  # IT hub with good education
        'Maharashtra': 1.02, # Industrial state with good schools
        'Gujarat': 1.0,     # Average performance
        'Punjab': 0.99,
        'Haryana': 0.98,
        'MP': 0.98,         # Developing education system
        'UP': 0.95,         # Large population, varied quality
        'Rajasthan': 0.96,
        'Bihar': 0.92,      # Challenges in education infrastructure
        'West Bengal': 0.97
    }
    
    # Apply board-based score adjustments
    board_adjustments = {
        'IB': 8,           # International Baccalaureate - premium education
        'ICSE': 5,         # Indian Certificate of Secondary Education - quality focus
        'CBSE': 3,         # Central Board - standardized, good quality
        'State Board': 0,  # Baseline
        'NIOS': -2         # National Institute of Open Schooling - flexible but challenging
    }
    
    # Apply test preparation adjustments
    prep_adjustments = {
        'coaching': 6,     # Professional coaching helps significantly
        'self-study': 3,   # Self-study provides moderate benefit
        'none': 0          # No additional preparation
    }
    
    # Apply all adjustments to base score
    final_scores = []
    for i, row in df.iterrows():
        score = base_score.iloc[i]
        
        # Apply state multiplier
        multiplier = state_multipliers.get(row['state'], 1.0)
        score *= multiplier
        
        # Apply board adjustment
        board_adj = board_adjustments.get(row['board_type'], 0)
        score += board_adj
        
        # Apply test preparation adjustment
        prep_adj = prep_adjustments.get(row['test_preparation'], 0)
        score += prep_adj
        
        # Add some random noise to make it realistic
        score += np.random.normal(0, 5)
        
        final_scores.append(score)
    
    # Cap final scores between 0 and 100
    df['final_score'] = np.clip(final_scores, 0, 100)
    
    return df

def train_model(model_type='decision_tree'):
    """
    Train the student performance prediction model
    
    Args:
        model_type (str): Type of model to train ('decision_tree' or 'linear_regression')
        
    Returns:
        tuple: Trained model and feature engineer
    """
    print("[TRAINING] Starting Student Performance Prediction Model Training...")
    print("=" * 60)
    
    # Generate synthetic training data
    print("[DATA] Generating synthetic student data...")
    df = generate_synthetic_data(n_samples=2000)
    print(f"[SUCCESS] Generated {len(df)} student records")
    
    # Display basic statistics about the generated data
    print(f"\n[STATS] Dataset Statistics:")
    print(f"   - Average final score: {df['final_score'].mean():.2f}")
    print(f"   - Score standard deviation: {df['final_score'].std():.2f}")
    print(f"   - Score range: {df['final_score'].min():.1f} - {df['final_score'].max():.1f}")
    
    # Separate features and target variable
    X = df.drop('final_score', axis=1)  # Features
    y = df['final_score']               # Target variable
    
    # Split data into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )
    print(f"\n[SPLIT] Data split: {len(X_train)} training, {len(X_test)} testing samples")
    
    # Initialize and apply feature engineering
    print("\n[PREPROCESSING] Preprocessing features...")
    feature_engineer = FeatureEngineer()
    X_train_processed = feature_engineer.fit_transform(X_train)
    X_test_processed = feature_engineer.transform(X_test)
    
    print(f"[SUCCESS] Features processed: {X_train_processed.shape[1]} total features after encoding")
    
    # Initialize and train the model
    print(f"\n[MODEL] Training {model_type.replace('_', ' ').title()} model...")
    
    if model_type == 'decision_tree':
        # Decision Tree Regressor with optimized parameters
        model = DecisionTreeRegressor(
            max_depth=10,           # Prevent overfitting
            min_samples_split=20,   # Minimum samples to split a node
            min_samples_leaf=10,    # Minimum samples in leaf node
            random_state=42
        )
    else:
        # Linear Regression as alternative
        model = LinearRegression()
    
    # Train the model
    model.fit(X_train_processed, y_train)
    print("[SUCCESS] Model training completed!")
    
    # Make predictions on test set
    print("\n[EVALUATION] Evaluating model performance...")
    y_pred = model.predict(X_test_processed)
    
    # Cap predictions at 100 (maximum possible score)
    y_pred = np.clip(y_pred, 0, 100)
    
    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)           # Mean Absolute Error
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Root Mean Square Error
    r2 = r2_score(y_test, y_pred)                       # R-squared Score
    
    # Display evaluation results
    print("\n" + "=" * 40)
    print("[RESULTS] MODEL EVALUATION RESULTS")
    print("=" * 40)
    print(f"[MAE] Mean Absolute Error:  {mae:.2f} points")
    print(f"[RMSE] Root Mean Square Error: {rmse:.2f} points")
    print(f"[R2] R-squared Score: {r2:.3f} ({r2*100:.1f}%)")
    print("=" * 40)
    
    # Interpretation of results
    print("\n[INTERPRETATION] Model Performance Interpretation:")
    if mae < 5:
        print("   [EXCELLENT] Very accurate predictions")
    elif mae < 10:
        print("   [GOOD] Reasonably accurate predictions")
    elif mae < 15:
        print("   [FAIR] Moderate accuracy, room for improvement")
    else:
        print("   [POOR] Low accuracy, needs significant improvement")
    
    if r2 > 0.8:
        print("   [HIGH] High explanatory power - model captures patterns well")
    elif r2 > 0.6:
        print("   [MODERATE] Moderate explanatory power - decent pattern recognition")
    else:
        print("   [LOW] Low explanatory power - may need more features or different approach")
    
    # Save the trained model and feature engineer
    model_path = os.path.join(os.path.dirname(__file__), 'student_model.joblib')
    model_data = {
        'model': model,
        'feature_engineer': feature_engineer,
        'model_type': model_type,
        'training_metrics': {
            'mae': mae,
            'rmse': rmse,
            'r2_score': r2
        }
    }
    
    joblib.dump(model_data, model_path)
    print(f"\n[SAVE] Model saved successfully at: {model_path}")
    
    # Display feature importance for Decision Tree
    if model_type == 'decision_tree' and hasattr(model, 'feature_importances_'):
        print("\n[FEATURES] Top 10 Most Important Features:")
        feature_names = X_train_processed.columns
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for i, (_, row) in enumerate(importance_df.head(10).iterrows()):
            print(f"   {i+1:2d}. {row['feature']:<25} ({row['importance']:.3f})")
    
    print("\n[COMPLETE] Model training completed successfully!")
    return model, feature_engineer

def main():
    """Main function to run model training"""
    try:
        # Train Decision Tree model (default)
        model, feature_engineer = train_model('decision_tree')
        
        print("\n" + "="*60)
        print("[READY] Ready for predictions! Use predictor.py to make predictions.")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    main()