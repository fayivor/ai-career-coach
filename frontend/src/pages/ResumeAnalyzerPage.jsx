import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FaFileUpload, FaCheckCircle } from 'react-icons/fa';
import { analyzeResume } from '../services/api';

export default function ResumeAnalyzerPage() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const result = await analyzeResume(file);
      setAnalysis(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Resume Analyzer</h2>

      <div {...getRootProps()} className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${isDragActive ? 'border-primary bg-blue-50' : 'border-gray-300 hover:border-primary'}`}>
        <input {...getInputProps()} />
        <FaFileUpload className="mx-auto text-6xl text-gray-400 mb-4" />
        <p className="text-lg text-gray-600">
          {isDragActive ? 'Drop your resume here...' : 'Drag & drop your resume here, or click to select'}
        </p>
        <p className="text-sm text-gray-500 mt-2">Supports PDF and DOCX files</p>
      </div>

      {loading && (
        <div className="mt-6 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing your resume...</p>
        </div>
      )}

      {error && (
        <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      {analysis && (
        <div className="mt-6 space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-3 flex items-center">
              <FaCheckCircle className="text-green-500 mr-2" />
              Summary
            </h3>
            <p className="text-gray-700">{analysis.summary}</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-3">Skills Detected</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.skills.map((skill, idx) => (
                <span key={idx} className="px-3 py-1 bg-primary text-white rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {analysis.experience.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Experience</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                {analysis.experience.map((exp, idx) => (
                  <li key={idx}>{exp}</li>
                ))}
              </ul>
            </div>
          )}

          {analysis.education.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Education</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                {analysis.education.map((edu, idx) => (
                  <li key={idx}>{edu}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
