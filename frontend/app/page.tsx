"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    try {
      if (!file) {
        alert("Please select a PDF file");
        return;
      }

      setLoading(true);
      setResult("");

      const formData = new FormData();

      // IMPORTANT: backend expects key name "file"
      formData.append("file", file);

      const response = await fetch(
        "https://study-planner-2-cwxx.onrender.com/ask",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log(data);

      if (!response.ok) {
        setResult(data.detail || "Something went wrong");
      } else {
        setResult(data.study_plan || "No study plan received");
      }
    } catch (error) {
      console.error(error);
      setResult("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-xl p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          AI Study Planner
        </h1>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              setFile(e.target.files[0]);
            }
          }}
          className="mb-4"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg"
        >
          {loading ? "Generating..." : "Generate Study Plan"}
        </button>

        {result && (
          <div className="mt-6 bg-gray-100 p-4 rounded-lg whitespace-pre-wrap">
            {result}
          </div>
        )}
      </div>
    </main>
  );
}
