class StudentScorePredictor:
    def __init__(self):
        self.state_multipliers = {
            # High performing states
            'Tamil Nadu': 1.05, 'Kerala': 1.05, 'Maharashtra': 1.05, 'Delhi': 1.05,
            # Good performing states
            'Karnataka': 1.02, 'Gujarat': 1.02, 'Telangana': 1.02, 'West Bengal': 1.02,
            # Average performing states
            'Goa': 1.00, 'Punjab': 1.00, 'Haryana': 1.00, 'Himachal Pradesh': 1.00,
            'Uttarakhand': 1.00, 'Chandigarh': 1.00, 'Puducherry': 1.00, 'Andhra Pradesh': 1.00,
            # Lower performing states
            'Madhya Pradesh': 0.97, 'Uttar Pradesh': 0.96, 'Bihar': 0.94, 'Rajasthan': 0.98, 'Jharkhand': 0.95,
            'Chhattisgarh': 0.96, 'Odisha': 0.97,
            # North-East states
            'Nagaland': 0.92, 'Arunachal Pradesh': 0.92, 'Manipur': 0.93, 'Mizoram': 0.93,
            'Tripura': 0.94, 'Meghalaya': 0.92, 'Sikkim': 0.95, 'Assam': 0.95,
            # Union Territories
            'Jammu and Kashmir': 0.96, 'Ladakh': 0.94, 'Lakshadweep': 0.93, 'Andaman and Nicobar Islands': 0.94,
            'Dadra and Nagar Haveli and Daman and Diu': 0.98
        }
        
        self.school_type_scores = {
            'Government': -5, 'Private': 5, 'Semi-Government': 0
        }
        
        self.medium_scores = {
            'English': 5, 'Hindi': 0, 'Regional': -2
        }
        
        self.board_scores = {
            'CBSE': 3, 'ICSE': 5, 'IB': 8, 'Cambridge': 8, 'Edexcel': 8,
            'NIOS': -2, 'State Board': -3, 'MP Board': -4, 'UP Board': -4, 'Bihar Board': -5,
            'Madarsa Board': -6, 'Sanskrit Board': -6,
            'International Board': 6, 'NWAC': 6, 'Mauritius Board': 6, 'Nepal Board': 6,
            'Tamil Nadu Board': -2, 'Kerala Board': -2, 'Karnataka Board': -2,
            'Maharashtra Board': -2, 'Gujarat Board': -3, 'Rajasthan Board': -4,
            'West Bengal Board': -3, 'Andhra Pradesh Board': -3, 'Telangana Board': -3,
            'Punjab Board': -3, 'Haryana Board': -3, 'Himachal Pradesh Board': -2,
            'Uttarakhand Board': -2, 'Jharkhand Board': -4, 'Chhattisgarh Board': -4,
            'Odisha Board': -3, 'Assam Board': -4, 'Goa Board': -2
        }
        
        self.prep_scores = {
            'Coaching': 8, 'Self-study': 3, 'Online': 5, 'None': 0
        }
    
    def predict(self, data):
        base_score = 50
        
        # School type contribution
        school_score = self.school_type_scores.get(data['school_type'], 0)
        
        # Medium contribution
        medium_score = self.medium_scores.get(data['medium_of_instruction'], 0)
        
        # Internet access
        internet_score = 3 if data['internet_access'] else 0
        
        # Study hours (scaled: hours * 2.5)
        study_score = data['study_hours_per_day'] * 2.5
        
        # Tuition classes
        tuition_score = 5 if data['tuition_classes'] else 0
        
        # Attendance rate (scaled: rate * 0.1)
        attendance_score = data['attendance_rate'] * 0.1
        
        # Test preparation
        prep_score = self.prep_scores.get(data['test_preparation'], 0)
        
        # Previous exam score (scaled: score * 0.2)
        previous_score_contrib = data['previous_exam_score'] * 0.2
        
        # Board type
        board_score = self.board_scores.get(data['board_type'], 0)
        
        # Calculate predicted score
        predicted_score = (base_score + school_score + medium_score + 
                         internet_score + study_score + tuition_score + 
                         attendance_score + prep_score + previous_score_contrib + 
                         board_score)
        
        # Apply state multiplier
        state_multiplier = self.state_multipliers.get(data['state'], 1.0)
        final_score = predicted_score * state_multiplier
        
        # Cap at 100
        return min(final_score, 100.0)