import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    try {
      setError(null);
      const formData = new FormData();
      formData.append('file', file);

      // Upload resume
      const resumeRes = await axios.post('{BACKEND_URL}/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Call /analyze API
      const jobRes = await axios.post('{BACKEND_URL}/api/job/analyze', {
        title: 'Sample Job Title',
        description: jobDesc,
        resume_keywords: resumeRes.data.keywords || [],
        resume_content: resumeRes.data.content || ""
      });

      setResponse({
        resume: resumeRes.data,
        analyze: jobRes.data,
        gptMatch: null  // reset GPT result
      });
    } catch (err) {
      setError('Error connecting to backend: ' + err.message);
    }
  };

  const handleGptMatch = async () => {
    try {
      setError(null);
      const formData = new FormData();
      formData.append('file', file);

      // Upload resume (again, because backend is stateless)
      const resumeRes = await axios.post('http://{BACKEND_URL}/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Call GPT Match API
      const gptRes = await axios.post('http://{BACKEND_URL}/api/job/gpt-match', {
        resume_content: resumeRes.data.content,
        job_description: jobDesc
      });

      setResponse({
        resume: resumeRes.data,
        analyze: null,  // reset analyze result
        gptMatch: gptRes.data
      });
    } catch (err) {
      setError('Error with GPT matching: ' + err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-4">CV Optimizer</h1>
      <div className="w-full max-w-md">
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Upload Resume (PDF/DOCX)</label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Job Description</label>
          <textarea
            placeholder="Paste job description here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
            rows="6"
          />
        </div>

        <div className="flex space-x-2">
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            disabled={!file || !jobDesc}
          >
            Analyze (SkillNer)
          </button>

          <button
            onClick={handleGptMatch}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            disabled={!file || !jobDesc}
          >
            GPT Skill Match
          </button>
        </div>
      </div>

      {response?.analyze && (
        <div className="mt-4 p-4 bg-white rounded shadow w-full max-w-md">
          <h2 className="text-lg font-bold">SkillNer Analysis Result</h2>
          <pre className="text-sm">{JSON.stringify(response.analyze, null, 2)}</pre>
        </div>
      )}

      {response?.gptMatch && (
        <div className="mt-4 p-4 bg-white rounded shadow w-full max-w-md">
          <h2 className="text-lg font-bold">GPT Match Result</h2>
          <p><strong>Resume Skills:</strong> {response.gptMatch.resume_skills?.join(", ")}</p>
          <p><strong>JD Skills:</strong> {response.gptMatch.jd_skills?.join(", ")}</p>
          <p><strong>Missing Skills:</strong> {response.gptMatch.missing_skills?.join(", ")}</p>
          <p><strong>Suggestions:</strong> {response.gptMatch.suggestions}</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded w-full max-w-md">
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
