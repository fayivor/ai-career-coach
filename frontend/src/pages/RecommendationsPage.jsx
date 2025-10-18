import { useState, useEffect } from 'react';
import { FaBook, FaExternalLinkAlt, FaClock, FaGraduationCap } from 'react-icons/fa';
import { getAllCourses } from '../services/api';

export default function RecommendationsPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const data = await getAllCourses();
      setCourses(data.courses);
    } catch (error) {
      console.error('Failed to load courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCourses = filter === 'all'
    ? courses
    : courses.filter(c => c.level.toLowerCase() === filter);

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Course Recommendations</h2>

      <div className="mb-6 flex space-x-2">
        {['all', 'beginner', 'intermediate', 'advanced'].map((level) => (
          <button
            key={level}
            onClick={() => setFilter(level)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === level
                ? 'bg-primary text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            {level.charAt(0).toUpperCase() + level.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <FaBook className="text-3xl text-primary" />
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  course.level === 'Beginner' ? 'bg-green-100 text-green-800' :
                  course.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {course.level}
                </span>
              </div>

              <h3 className="text-lg font-bold text-gray-800 mb-2">{course.title}</h3>

              <div className="flex items-center text-sm text-gray-600 mb-2">
                <FaGraduationCap className="mr-2" />
                {course.provider}
              </div>

              <div className="flex items-center text-sm text-gray-600 mb-4">
                <FaClock className="mr-2" />
                {course.duration}
              </div>

              <div className="mb-4">
                <p className="text-sm text-gray-500 mb-2">Skills covered:</p>
                <div className="flex flex-wrap gap-1">
                  {course.skills_covered.slice(0, 3).map((skill, i) => (
                    <span key={i} className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                      {skill}
                    </span>
                  ))}
                  {course.skills_covered.length > 3 && (
                    <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                      +{course.skills_covered.length - 3} more
                    </span>
                  )}
                </div>
              </div>

              <a
                href={course.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center space-x-2 w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary transition-colors"
              >
                <span>View Course</span>
                <FaExternalLinkAlt />
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
