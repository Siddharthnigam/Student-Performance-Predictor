const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const studentAPI = {
  async predict(studentData) {
    const response = await fetch(`${API_BASE_URL}/predict/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(studentData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  },

  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health/`);
    return await response.json();
  }
};