from .ml_core.prediction_logic import StudentScorePredictor

predictor = StudentScorePredictor()

def predict_student_score(data):
    return predictor.predict(data)