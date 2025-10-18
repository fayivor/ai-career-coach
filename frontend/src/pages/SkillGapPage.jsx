import { useState, useEffect } from 'react';
import { FaSearch, FaChartPie } from 'react-icons/fa';
import { analyzeSkillGap, getAvailableRoles } from '../services/api';

export default function SkillGapPage() {
  const [roles, setRoles] = useState([]);
  const [currentSkills, setCurrentSkills] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    try {
      const data = await getAvailableRoles();
      setRoles(data.roles);
      if (data.roles.length > 0) {
        setTargetRole(data.roles[0]);
      }
    } catch (error) {
      console.error('Failed to load roles:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!currentSkills.trim() || !targetRole) return;

    setLoading(true);
    try {
      const skillsArray = currentSkills.split(',').map(s => s.trim()).filter(s => s);
      const result = await analyzeSkillGap(skillsArray, targetRole);
      setAnalysis(result);
    } catch (error) {
      alert('Failed to analyze skill gap');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Skill Gap Analysis</h2>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Current Skills (comma-separated)
            </label>
            <textarea
              value={currentSkills}
              onChange={(e) => setCurrentSkills(e.target.value)}
              placeholder="e.g., Python, JavaScript, SQL, React"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              rows="3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Role
            </label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {roles.map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading || !currentSkills.trim()}
            className="w-full px-6 py-3 bg-primary text-white rounded-lg hover:bg-secondary transition-colors disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            <FaSearch />
            <span>{loading ? 'Analyzing...' : 'Analyze Skill Gap'}</span>
          </button>
        </div>
      </div>

      {analysis && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <FaChartPie className="text-primary mr-2" />
              Gap Analysis: {analysis.gap_percentage}% Gap
            </h3>

            <div className="mb-4">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Skill Match</span>
                <span>{100 - analysis.gap_percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-green-500 h-4 rounded-full transition-all"
                  style={{ width: `${100 - analysis.gap_percentage}%` }}
                />
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-bold text-green-600 mb-3">
                Matched Skills ({analysis.matched_skills.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {analysis.matched_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-bold text-red-600 mb-3">
                Missing Skills ({analysis.missing_skills.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {analysis.recommendations.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Recommendations</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                {analysis.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
