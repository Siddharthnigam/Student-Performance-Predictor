const PredictionResult = ({ result, error }) => {
  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-6 p-6 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!result) return null;

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    if (score >= 60) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 90) return 'bg-green-50 border-green-200';
    if (score >= 80) return 'bg-blue-50 border-blue-200';
    if (score >= 70) return 'bg-yellow-50 border-yellow-200';
    if (score >= 60) return 'bg-orange-50 border-orange-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="max-w-2xl mx-auto mt-6 space-y-4">
      {/* Score Display */}
      <div className={`p-6 border rounded-lg ${getScoreBg(result.predicted_score)}`}>
        <div className="text-center">
          <h3 className="text-2xl font-bold text-gray-800 mb-2">Predicted Score</h3>
          <div className={`text-6xl font-bold ${getScoreColor(result.predicted_score)}`}>
            {result.predicted_score}
          </div>
          <div className="text-lg text-gray-600 mt-2">out of 100</div>
          <div className="text-sm text-gray-500 mt-1">
            {result.performance_category}
          </div>
        </div>
      </div>

      {/* Key Factors */}
      {result.key_factors && result.key_factors.length > 0 && (
        <div className="p-6 bg-white border border-gray-200 rounded-lg">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">Key Factors</h4>
          <ul className="space-y-2">
            {result.key_factors.map((factor, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-500 mr-2">•</span>
                <span className="text-gray-700">{factor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <div className="p-6 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="text-lg font-semibold text-blue-800 mb-3">Recommendations</h4>
          <ul className="space-y-2">
            {result.recommendations.map((rec, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-600 mr-2">→</span>
                <span className="text-blue-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Confidence Level */}
      {result.confidence_level && (
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="text-sm text-gray-600">
            <strong>Confidence Level:</strong> {result.confidence_level}
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionResult;