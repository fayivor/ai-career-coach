import { useState, useEffect } from 'react';
import { FaPlus, FaTrash, FaCheck, FaClock, FaChartBar } from 'react-icons/fa';
import { getGoals, createGoal, updateGoal, deleteGoal, getTrackerStats } from '../services/api';

export default function TrackerPage() {
  const [goals, setGoals] = useState([]);
  const [stats, setStats] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    target_date: ''
  });

  useEffect(() => {
    loadGoals();
    loadStats();
  }, []);

  const loadGoals = async () => {
    try {
      const data = await getGoals();
      setGoals(data);
    } catch (error) {
      console.error('Failed to load goals:', error);
    }
  };

  const loadStats = async () => {
    try {
      const data = await getTrackerStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createGoal(formData);
      setFormData({ title: '', description: '', target_date: '' });
      setShowForm(false);
      loadGoals();
      loadStats();
    } catch (error) {
      alert('Failed to create goal');
    }
  };

  const handleStatusChange = async (goalId, newStatus) => {
    try {
      await updateGoal(goalId, { status: newStatus });
      loadGoals();
      loadStats();
    } catch (error) {
      alert('Failed to update goal');
    }
  };

  const handleDelete = async (goalId) => {
    if (!confirm('Are you sure you want to delete this goal?')) return;
    try {
      await deleteGoal(goalId);
      loadGoals();
      loadStats();
    } catch (error) {
      alert('Failed to delete goal');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">Career Goals Tracker</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary transition-colors flex items-center space-x-2"
        >
          <FaPlus />
          <span>New Goal</span>
        </button>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <StatCard title="Total Goals" value={stats.total_goals} icon={<FaChartBar />} color="bg-blue-500" />
          <StatCard title="Pending" value={stats.pending} icon={<FaClock />} color="bg-yellow-500" />
          <StatCard title="In Progress" value={stats.in_progress} icon={<FaClock />} color="bg-orange-500" />
          <StatCard title="Completed" value={stats.completed} icon={<FaCheck />} color="bg-green-500" />
        </div>
      )}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Create New Goal</h3>
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Goal title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <textarea
              placeholder="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              rows="3"
            />
            <input
              type="date"
              value={formData.target_date}
              onChange={(e) => setFormData({ ...formData, target_date: e.target.value })}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <div className="flex space-x-2">
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary transition-colors"
              >
                Create Goal
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </form>
      )}

      <div className="space-y-4">
        {goals.map((goal) => (
          <div key={goal.id} className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-xl font-bold text-gray-800">{goal.title}</h3>
              <button
                onClick={() => handleDelete(goal.id)}
                className="text-red-500 hover:text-red-700"
              >
                <FaTrash />
              </button>
            </div>
            <p className="text-gray-600 mb-3">{goal.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">Target: {goal.target_date}</span>
              <select
                value={goal.status}
                onChange={(e) => handleStatusChange(goal.id, e.target.value)}
                className={`px-3 py-1 rounded-lg text-sm font-medium ${
                  goal.status === 'completed' ? 'bg-green-100 text-green-800' :
                  goal.status === 'in_progress' ? 'bg-orange-100 text-orange-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        ))}
      </div>

      {goals.length === 0 && !showForm && (
        <div className="text-center py-12 text-gray-500">
          No goals yet. Click "New Goal" to create one!
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, icon, color }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${color} text-white`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
