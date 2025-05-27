import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    try {
      setError(null);
      // Create form data for resume upload
      const formData = new FormData();
      formData.append('file', file);

      // Send resume to backend
      const resumeRes = await axios.post('http://34.219.209.95:8000/api/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Send job description to backend, including resume keywords
      const jobRes = await axios.post('http://34.219.209.95:8000/api/job/analyze', {
        title: 'Sample Job Title',
        description: jobDesc,
        resume_keywords: resumeRes.data.keywords || []
      });

      // Store responses
      setResponse({ resume: resumeRes.data, job: jobRes.data });
    } catch (err) {
      setError('Error connecting to backend: ' + err.message);
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
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          disabled={!file || !jobDesc}
        >
          Submit
        </button>
      </div>
      {response && (
        <div className="mt-4 p-4 bg-white rounded shadow w-full max-w-md">
          <h2 className="text-lg font-bold">Backend Response</h2>
          <pre className="text-sm">{JSON.stringify(response, null, 2)}</pre>
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
