import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { FaRobot, FaFileAlt, FaChartLine, FaBook, FaTasks } from 'react-icons/fa';
import ChatbotPage from './pages/ChatbotPage';
import ResumeAnalyzerPage from './pages/ResumeAnalyzerPage';
import SkillGapPage from './pages/SkillGapPage';
import RecommendationsPage from './pages/RecommendationsPage';
import TrackerPage from './pages/TrackerPage';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  AI Career Coach
                </h1>
              </div>
              <div className="flex space-x-4">
                <NavLink to="/" icon={<FaRobot />} text="Chatbot" />
                <NavLink to="/resume" icon={<FaFileAlt />} text="Resume" />
                <NavLink to="/skills" icon={<FaChartLine />} text="Skills" />
                <NavLink to="/recommendations" icon={<FaBook />} text="Courses" />
                <NavLink to="/tracker" icon={<FaTasks />} text="Tracker" />
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<ChatbotPage />} />
            <Route path="/resume" element={<ResumeAnalyzerPage />} />
            <Route path="/skills" element={<SkillGapPage />} />
            <Route path="/recommendations" element={<RecommendationsPage />} />
            <Route path="/tracker" element={<TrackerPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function NavLink({ to, icon, text }) {
  return (
    <Link
      to={to}
      className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-primary hover:text-white transition-colors"
    >
      {icon}
      <span>{text}</span>
    </Link>
  );
}

export default App;
