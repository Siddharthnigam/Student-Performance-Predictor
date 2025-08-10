import { useState } from 'react';

const StudentForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    state: 'Maharashtra',
    school_type: 'private',
    medium_of_instruction: 'English',
    internet_access: true,
    study_hours_per_day: 6,
    tuition_classes: true,
    attendance_rate: 85,
    test_preparation: 'coaching',
    previous_exam_score: 75,
    board_type: 'CBSE'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              type === 'number' ? parseFloat(value) : value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
        Student Performance Prediction
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
          <select name="state" value={formData.state} onChange={handleChange}
                  className="w-full p-2 border border-gray-300 rounded-md">
            <option value="Maharashtra">Maharashtra</option>
            <option value="MP">MP</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Karnataka">Karnataka</option>
            <option value="UP">UP</option>
            <option value="Bihar">Bihar</option>
            <option value="Kerala">Kerala</option>
            <option value="Gujarat">Gujarat</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">School Type</label>
          <select name="school_type" value={formData.school_type} onChange={handleChange}
                  className="w-full p-2 border border-gray-300 rounded-md">
            <option value="government">Government</option>
            <option value="private">Private</option>
            <option value="aided">Aided</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Medium of Instruction</label>
          <select name="medium_of_instruction" value={formData.medium_of_instruction} onChange={handleChange}
                  className="w-full p-2 border border-gray-300 rounded-md">
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="regional">Regional</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Board Type</label>
          <select name="board_type" value={formData.board_type} onChange={handleChange}
                  className="w-full p-2 border border-gray-300 rounded-md">
            <option value="CBSE">CBSE</option>
            <option value="ICSE">ICSE</option>
            <option value="State Board">State Board</option>
            <option value="IB">IB</option>
            <option value="NIOS">NIOS</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Study Hours per Day</label>
          <input type="number" name="study_hours_per_day" value={formData.study_hours_per_day}
                 onChange={handleChange} min="0" max="24" step="0.5"
                 className="w-full p-2 border border-gray-300 rounded-md" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Attendance Rate (%)</label>
          <input type="number" name="attendance_rate" value={formData.attendance_rate}
                 onChange={handleChange} min="0" max="100"
                 className="w-full p-2 border border-gray-300 rounded-md" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Previous Exam Score</label>
          <input type="number" name="previous_exam_score" value={formData.previous_exam_score}
                 onChange={handleChange} min="0" max="100"
                 className="w-full p-2 border border-gray-300 rounded-md" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Test Preparation</label>
          <select name="test_preparation" value={formData.test_preparation} onChange={handleChange}
                  className="w-full p-2 border border-gray-300 rounded-md">
            <option value="none">None</option>
            <option value="self-study">Self Study</option>
            <option value="coaching">Coaching</option>
          </select>
        </div>

        <div className="flex items-center space-x-4">
          <label className="flex items-center">
            <input type="checkbox" name="internet_access" checked={formData.internet_access}
                   onChange={handleChange} className="mr-2" />
            Internet Access
          </label>
          
          <label className="flex items-center">
            <input type="checkbox" name="tuition_classes" checked={formData.tuition_classes}
                   onChange={handleChange} className="mr-2" />
            Tuition Classes
          </label>
        </div>
      </div>

      <button type="submit" disabled={loading}
              className="w-full mt-6 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50">
        {loading ? 'Predicting...' : 'Predict Performance'}
      </button>
    </form>
  );
};

export default StudentForm;