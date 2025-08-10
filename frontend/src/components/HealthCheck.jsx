import { useState, useEffect } from 'react';
import { studentAPI } from '../services/api';

const HealthCheck = () => {
  const [status, setStatus] = useState('checking');
  const [health, setHealth] = useState(null);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const result = await studentAPI.healthCheck();
      setHealth(result);
      setStatus(result.success ? 'healthy' : 'unhealthy');
    } catch (error) {
      setStatus('error');
      setHealth({ error: error.message });
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'healthy': return 'text-green-600';
      case 'unhealthy': return 'text-yellow-600';
      case 'error': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="mb-4 p-3 bg-white rounded-lg shadow-sm border">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">API Status:</span>
        <div className={`text-sm font-semibold ${getStatusColor()}`}>
          {status === 'checking' ? 'Checking...' : 
           status === 'healthy' ? '● Online' :
           status === 'unhealthy' ? '● Limited' : '● Offline'}
        </div>
      </div>
      {health?.message && (
        <div className="text-xs text-gray-500 mt-1">{health.message}</div>
      )}
    </div>
  );
};

export default HealthCheck;