/**
 * Frontend Integration Example for Student Performance Prediction API
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// React Hook for Student Prediction
const useStudentPredictor = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const predict = async (studentData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/predict/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentData)
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return { predict, loading, result, error };
};

// Vanilla JavaScript Example
class StudentPredictor {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async predict(studentData) {
    try {
      const response = await fetch(`${this.baseUrl}/predict/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentData)
      });

      return await response.json();
    } catch (error) {
      throw new Error('Prediction failed: ' + error.message);
    }
  }

  async batchPredict(students) {
    try {
      const response = await fetch(`${this.baseUrl}/predict/batch/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ students })
      });

      return await response.json();
    } catch (error) {
      throw new Error('Batch prediction failed: ' + error.message);
    }
  }

  async getModelInfo() {
    try {
      const response = await fetch(`${this.baseUrl}/model/info/`);
      return await response.json();
    } catch (error) {
      throw new Error('Failed to get model info: ' + error.message);
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/health/`);
      return await response.json();
    } catch (error) {
      throw new Error('Health check failed: ' + error.message);
    }
  }
}

// Usage Examples
const examples = {
  // Single prediction
  singlePrediction: async () => {
    const predictor = new StudentPredictor();
    
    const studentData = {
      state: 'Maharashtra',
      school_type: 'private',
      medium_of_instruction: 'English',
      internet_access: true,
      study_hours_per_day: 6.0,
      tuition_classes: true,
      attendance_rate: 90.0,
      test_preparation: 'coaching',
      previous_exam_score: 85.0,
      board_type: 'CBSE'
    };

    const result = await predictor.predict(studentData);
    console.log(`Predicted Score: ${result.predicted_score}/100`);
    console.log(`Category: ${result.performance_category}`);
  },

  // Batch prediction
  batchPrediction: async () => {
    const predictor = new StudentPredictor();
    
    const students = [
      {
        state: 'Maharashtra',
        school_type: 'private',
        previous_exam_score: 85.0,
        // ... other fields
      },
      {
        state: 'Bihar',
        school_type: 'government',
        previous_exam_score: 55.0,
        // ... other fields
      }
    ];

    const result = await predictor.batchPredict(students);
    result.results.forEach((student, index) => {
      console.log(`Student ${index}: ${student.predicted_score}/100`);
    });
  }
};

// Export for use in React/Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { StudentPredictor, useStudentPredictor };
}