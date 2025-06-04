import React, { useState } from 'react';
import axios from 'axios';

export default function RagUI() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleQuery = async () => {
    try {
      const res = await axios.post('http://localhost:8082/query', { query });
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer('Error querying RAG agent.');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8081/upload', formData);
      setUploadStatus('✅ Uploaded successfully');
    } catch (err) {
      setUploadStatus('❌ Upload failed');
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🧠 Private RAG Interface</h1>

      <div className="mb-4">
        <input
          type="text"
          className="w-full p-2 border rounded"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleQuery}
          className="mt-2 bg-blue-600 text-white px-4 py-2 rounded"
        >
          Query</button>
      </div>

      {answer && (
        <div className="mb-6 p-3 border rounded bg-gray-100">
          <h2 className="font-semibold">📘 Answer:</h2>
          <p>{answer}</p>
        </div>
      )}

      <div className="mb-4">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-2"
        />
        <button
          onClick={handleUpload}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Upload</button>
        <p>{uploadStatus}</p>
      </div>
    </div>
  );
}
