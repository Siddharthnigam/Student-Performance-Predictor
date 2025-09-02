import { useState } from "react";
import axios from "axios";

export default function PredictionForm() {
  const [formData, setFormData] = useState({
    state: "",
    school_type: "",
    medium_of_instruction: "",
    internet_access: false,
    study_hours_per_day: "",
    tuition_classes: false,
    attendance_rate: "",
    test_preparation: "",
    previous_exam_score: "",
    board_type: ""
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({ 
      ...formData, 
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    // Validate and convert numeric fields
    if (!formData.study_hours_per_day || !formData.attendance_rate || !formData.previous_exam_score) {
      setError('Please fill in all numeric fields');
      setLoading(false);
      return;
    }
    
    const submitData = {
      ...formData,
      study_hours_per_day: parseFloat(formData.study_hours_per_day),
      attendance_rate: parseFloat(formData.attendance_rate),
      previous_exam_score: parseFloat(formData.previous_exam_score)
    };
    
    try {
      const res = await axios.post("https://student-performance-predictor-1-n1oy.onrender.com/api/predict/", submitData);
      setResult(res.data.prediction);
    } catch (err) {
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object' && !errorData.error) {
          const errorMessages = Object.entries(errorData).map(([field, messages]) => 
            `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
          ).join('; ');
          setError(`Validation errors: ${errorMessages}`);
        } else {
          setError(errorData.error || JSON.stringify(errorData));
        }
      } else {
        setError(err.message);
      }
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Student Performance Predictor</h2>
      
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
          <select name="state" value={formData.state} onChange={handleChange} className="border border-gray-300 p-3 w-full rounded-md" required>
            <option value="">Select State</option>
            <optgroup label="High Performing States">
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Kerala">Kerala</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Delhi">Delhi</option>
            </optgroup>
            <optgroup label="Good Performing States">
              <option value="Karnataka">Karnataka</option>
              <option value="Gujarat">Gujarat</option>
              <option value="Telangana">Telangana</option>
              <option value="West Bengal">West Bengal</option>
            </optgroup>
            <optgroup label="Average Performing States">
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Goa">Goa</option>
              <option value="Punjab">Punjab</option>
              <option value="Haryana">Haryana</option>
              <option value="Himachal Pradesh">Himachal Pradesh</option>
              <option value="Uttarakhand">Uttarakhand</option>
            </optgroup>
            <optgroup label="Developing States">
              <option value="Madhya Pradesh">Madhya Pradesh</option>
              <option value="Uttar Pradesh">Uttar Pradesh</option>
              <option value="Bihar">Bihar</option>
              <option value="Rajasthan">Rajasthan</option>
              <option value="Jharkhand">Jharkhand</option>
              <option value="Chhattisgarh">Chhattisgarh</option>
              <option value="Odisha">Odisha</option>
            </optgroup>
            <optgroup label="North-East States">
              <option value="Assam">Assam</option>
              <option value="Nagaland">Nagaland</option>
              <option value="Arunachal Pradesh">Arunachal Pradesh</option>
              <option value="Manipur">Manipur</option>
              <option value="Mizoram">Mizoram</option>
              <option value="Tripura">Tripura</option>
              <option value="Meghalaya">Meghalaya</option>
              <option value="Sikkim">Sikkim</option>
            </optgroup>
            <optgroup label="Union Territories">
              <option value="Chandigarh">Chandigarh</option>
              <option value="Puducherry">Puducherry</option>
              <option value="Jammu and Kashmir">Jammu and Kashmir</option>
              <option value="Ladakh">Ladakh</option>
              <option value="Lakshadweep">Lakshadweep</option>
              <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
              <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
            </optgroup>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">School Type</label>
          <select name="school_type" value={formData.school_type} onChange={handleChange} className="border border-gray-300 p-3 w-full rounded-md" required>
            <option value="">Select School Type</option>
            <option value="Government">Government</option>
            <option value="Private">Private</option>
            <option value="Semi-Government">Semi-Government</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Medium of Instruction</label>
          <select name="medium_of_instruction" value={formData.medium_of_instruction} onChange={handleChange} className="border border-gray-300 p-3 w-full rounded-md" required>
            <option value="">Select Medium</option>
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="Regional">Regional Language</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Board Type</label>
          <select name="board_type" value={formData.board_type} onChange={handleChange} className="border border-gray-300 p-3 w-full rounded-md" required>
            <option value="">Select Board</option>
            <optgroup label="National Boards">
              <option value="CBSE">CBSE</option>
              <option value="ICSE">ICSE</option>
              <option value="NIOS">NIOS (Open Schooling)</option>
            </optgroup>
            <optgroup label="International Boards">
              <option value="IB">IB (International Baccalaureate)</option>
              <option value="Cambridge">Cambridge</option>
              <option value="Edexcel">Edexcel</option>
              <option value="International Board">Other International Board</option>
            </optgroup>
            <optgroup label="State Boards">
              <option value="State Board">General State Board</option>
              <option value="Maharashtra Board">Maharashtra Board</option>
              <option value="Tamil Nadu Board">Tamil Nadu Board</option>
              <option value="Kerala Board">Kerala Board</option>
              <option value="Karnataka Board">Karnataka Board</option>
              <option value="Gujarat Board">Gujarat Board</option>
              <option value="West Bengal Board">West Bengal Board</option>
              <option value="Andhra Pradesh Board">Andhra Pradesh Board</option>
              <option value="Telangana Board">Telangana Board</option>
              <option value="MP Board">MP Board</option>
              <option value="UP Board">UP Board</option>
              <option value="Bihar Board">Bihar Board</option>
              <option value="Rajasthan Board">Rajasthan Board</option>
              <option value="Punjab Board">Punjab Board</option>
              <option value="Haryana Board">Haryana Board</option>
              <option value="Himachal Pradesh Board">Himachal Pradesh Board</option>
              <option value="Uttarakhand Board">Uttarakhand Board</option>
              <option value="Jharkhand Board">Jharkhand Board</option>
              <option value="Chhattisgarh Board">Chhattisgarh Board</option>
              <option value="Odisha Board">Odisha Board</option>
              <option value="Assam Board">Assam Board</option>
              <option value="Goa Board">Goa Board</option>
            </optgroup>
            <optgroup label="Specialized Boards">
              <option value="Madarsa Board">Madarsa Board</option>
              <option value="Sanskrit Board">Sanskrit Board</option>
            </optgroup>
            <optgroup label="Foreign Boards">
              <option value="NWAC">NWAC</option>
              <option value="Mauritius Board">Mauritius Board</option>
              <option value="Nepal Board">Nepal Board</option>
            </optgroup>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Study Hours per Day</label>
          <input
            name="study_hours_per_day"
            type="number"
            min="0"
            max="24"
            step="0.5"
            value={formData.study_hours_per_day}
            onChange={handleChange}
            placeholder="Hours per day"
            className="border border-gray-300 p-3 w-full rounded-md"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Attendance Rate (%)</label>
          <input
            name="attendance_rate"
            type="number"
            min="0"
            max="100"
            step="0.1"
            value={formData.attendance_rate}
            onChange={handleChange}
            placeholder="Attendance percentage"
            className="border border-gray-300 p-3 w-full rounded-md"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Previous Exam Score</label>
          <input
            name="previous_exam_score"
            type="number"
            min="0"
            max="100"
            step="0.1"
            value={formData.previous_exam_score}
            onChange={handleChange}
            placeholder="Previous score"
            className="border border-gray-300 p-3 w-full rounded-md"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Test Preparation</label>
          <select name="test_preparation" value={formData.test_preparation} onChange={handleChange} className="border border-gray-300 p-3 w-full rounded-md" required>
            <option value="">Select Preparation Type</option>
            <option value="Coaching">Coaching Classes</option>
            <option value="Self-study">Self Study</option>
            <option value="Online">Online Courses</option>
            <option value="None">None</option>
          </select>
        </div>
        
        <div className="flex items-center space-x-4">
          <label className="flex items-center">
            <input
              name="internet_access"
              type="checkbox"
              checked={formData.internet_access}
              onChange={handleChange}
              className="mr-2"
            />
            Internet Access
          </label>
          
          <label className="flex items-center">
            <input
              name="tuition_classes"
              type="checkbox"
              checked={formData.tuition_classes}
              onChange={handleChange}
              className="mr-2"
            />
            Tuition Classes
          </label>
        </div>
        
        <div className="md:col-span-2">
          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white py-3 px-4 rounded-md font-medium transition duration-200"
          >
            {loading ? "Calculating..." : "Predict Performance"}
          </button>
        </div>
      </form>
      
      {result !== null && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
          <p className="text-center text-lg font-semibold text-green-800">
            Predicted Score: {Math.round(result * 100) / 100}%
          </p>
        </div>
      )}
      
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-center text-sm text-red-600">
            Error: {error}
          </p>
        </div>
      )}
    </div>
  );
}