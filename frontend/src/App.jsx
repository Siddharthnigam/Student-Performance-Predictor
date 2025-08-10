import { useState } from 'react'
import StudentForm from './components/StudentForm'
import PredictionResult from './components/PredictionResult'
import HealthCheck from './components/HealthCheck'
import { studentAPI } from './services/api'

function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handlePredict = async (studentData) => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const prediction = await studentAPI.predict(studentData)
      setResult(prediction)
    } catch (err) {
      setError(err.message || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Student Performance Predictor
        </h1>
        
        <HealthCheck />
        <StudentForm onSubmit={handlePredict} loading={loading} />
        <PredictionResult result={result} error={error} />
      </div>
    </div>
  )
}

export default App
