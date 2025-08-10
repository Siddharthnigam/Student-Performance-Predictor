"""
Feature Engineering Module for Student Performance Prediction

This module handles all preprocessing tasks including:
- Categorical feature encoding (One-Hot Encoding)
- Numerical feature scaling (StandardScaler)
- Missing value imputation
- Boolean feature conversion

Author: Student Performance ML System
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import joblib

class FeatureEngineer:
    """
    Feature engineering class for preprocessing student data
    
    Handles encoding of categorical variables, scaling of numerical variables,
    and missing value imputation for the Indian education context.
    """
    
    def __init__(self):
        """Initialize the feature engineer with empty encoders and scaler"""
        self.encoders = {}  # Dictionary to store one-hot encoders for each categorical feature
        self.scaler = StandardScaler()  # Scaler for numerical features
        
        # Define feature categories for processing
        self.categorical_features = [
            'state', 'school_type', 'medium_of_instruction', 
            'test_preparation', 'board_type'
        ]
        
        self.numerical_features = [
            'study_hours_per_day', 'attendance_rate', 'previous_exam_score'
        ]
        
        self.boolean_features = [
            'internet_access', 'tuition_classes'
        ]
        
    def fit_transform(self, df):
        """
        Fit encoders on training data and transform it
        
        Args:
            df (pandas.DataFrame): Training dataframe with raw features
            
        Returns:
            pandas.DataFrame: Processed dataframe ready for model training
        """
        processed_df = df.copy()
        
        # Handle missing values with appropriate defaults for Indian education context
        processed_df = processed_df.fillna({
            'study_hours_per_day': processed_df['study_hours_per_day'].median(),
            'attendance_rate': processed_df['attendance_rate'].median(),
            'previous_exam_score': processed_df['previous_exam_score'].median(),
            'state': 'Unknown',  # Default state for missing values
            'school_type': 'government',  # Most common school type in India
            'medium_of_instruction': 'Hindi',  # Most common medium
            'test_preparation': 'none',  # Default preparation level
            'board_type': 'State Board'  # Most common board type
        })
        
        # Convert boolean features to integers (0/1)
        for col in self.boolean_features:
            processed_df[col] = processed_df[col].astype(int)
        
        # One-hot encode categorical features
        for col in self.categorical_features:
            # Create and fit encoder for this categorical feature
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            encoded = encoder.fit_transform(processed_df[[col]])
            self.encoders[col] = encoder  # Store encoder for later use
            
            # Create meaningful column names for encoded features
            col_names = [f"{col}_{cat}" for cat in encoder.categories_[0]]
            encoded_df = pd.DataFrame(encoded, columns=col_names, index=processed_df.index)
            
            # Replace original categorical column with encoded columns
            processed_df = processed_df.drop(col, axis=1)
            processed_df = pd.concat([processed_df, encoded_df], axis=1)
        
        # Scale numerical features to have mean=0 and std=1
        processed_df[self.numerical_features] = self.scaler.fit_transform(
            processed_df[self.numerical_features]
        )
        
        return processed_df
    
    def transform(self, df):
        """
        Transform new data using previously fitted encoders
        
        Args:
            df (pandas.DataFrame): New dataframe to transform
            
        Returns:
            pandas.DataFrame: Processed dataframe ready for prediction
        """
        processed_df = df.copy()
        
        # Handle missing values with same defaults as training
        processed_df = processed_df.fillna({
            'study_hours_per_day': 4.0,  # Average study hours
            'attendance_rate': 85.0,  # Average attendance
            'previous_exam_score': 75.0,  # Average previous score
            'state': 'Unknown',
            'school_type': 'government',
            'medium_of_instruction': 'Hindi',
            'test_preparation': 'none',
            'board_type': 'State Board'
        })
        
        # Convert boolean features to integers
        for col in self.boolean_features:
            processed_df[col] = processed_df[col].astype(int)
        
        # Apply previously fitted one-hot encoders
        for col in self.categorical_features:
            if col in self.encoders:
                encoded = self.encoders[col].transform(processed_df[[col]])
                col_names = [f"{col}_{cat}" for cat in self.encoders[col].categories_[0]]
                encoded_df = pd.DataFrame(encoded, columns=col_names, index=processed_df.index)
                
                # Replace original column with encoded columns
                processed_df = processed_df.drop(col, axis=1)
                processed_df = pd.concat([processed_df, encoded_df], axis=1)
        
        # Apply previously fitted scaler to numerical features
        processed_df[self.numerical_features] = self.scaler.transform(
            processed_df[self.numerical_features]
        )
        
        return processed_df
    
    def save(self, filepath):
        """
        Save the feature engineer to disk
        
        Args:
            filepath (str): Path to save the feature engineer
        """
        joblib.dump(self, filepath)
    
    @classmethod
    def load(cls, filepath):
        """
        Load a previously saved feature engineer
        
        Args:
            filepath (str): Path to load the feature engineer from
            
        Returns:
            FeatureEngineer: Loaded feature engineer instance
        """
        return joblib.load(filepath)