"use client";

import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [subject, setSubject] = useState("");
  const [days, setDays] = useState("");
  const [question, setQuestion] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState("");
  const [uploaded, setUploaded] = useState(false);

  async function uploadPDF() {
    if (!file) return alert("Please select a PDF first");

    const formData = new FormData();
    formData.append("file", file);

    setLoading("Uploading PDF...");
    setOutput("");

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setUploaded(true);
      setOutput(`✅ ${data.message}\nCharacters extracted: ${data.characters_extracted}`);
    } catch {
      setOutput("❌ Upload failed. Check backend server.");
    }

    setLoading("");
  }

  async function generatePlan() {
    if (!uploaded) return alert("Upload PDF first");
    if (!subject || !days) return alert("Enter subject and days");

    const formData = new FormData();
    formData.append("subject", subject);
    formData.append("days", days);

    setLoading("Generating study plan...");
    setOutput("");

    try {
      const res = await fetch(`${API_URL}/generate-plan`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setOutput(data.result || data.error);
    } catch {
      setOutput("❌ Failed to generate study plan.");
    }

    setLoading("");
  }

  async function askQuestion() {
    if (!uploaded) return alert("Upload PDF first");
    if (!question) return alert("Enter your question");

    const formData = new FormData();
    formData.append("question", question);

    setLoading("Finding answer...");
    setOutput("");

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setOutput(data.answer || data.error);
    } catch {
      setOutput("❌ Failed to answer question.");
    }

    setLoading("");
  }

  async function generateMCQ() {
    if (!uploaded) return alert("Upload PDF first");

    setLoading("Generating MCQs and flashcards...");
    setOutput("");

    try {
      const res = await fetch(`${API_URL}/generate-mcq`, {
        method: "POST",
      });

      const data = await res.json();
      setOutput(data.result || data.error);
    } catch {
      setOutput("❌ Failed to generate MCQs.");
    }

    setLoading("");
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 text-white px-6 py-8">
      <div className="mx-auto max-w-6xl">
        <section className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-bold mb-3">
            AI Study Planner
          </h1>
          <p className="text-slate-300">
            Upload your notes and let AI agents create study plans, answers,
            MCQs, and flashcards.
          </p>
        </section>

        <div className="grid md:grid-cols-2 gap-6">
          <section className="bg-white/10 backdrop-blur-xl rounded-3xl p-6 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold mb-4">Upload Document</h2>

            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full mb-4 rounded-xl bg-white/10 p-3 text-sm"
            />

            <button
              onClick={uploadPDF}
              className="w-full rounded-xl bg-indigo-500 hover:bg-indigo-600 transition p-3 font-semibold"
            >
              Upload PDF
            </button>

            {uploaded && (
              <p className="mt-4 text-green-400 font-medium">
                ✅ PDF uploaded successfully
              </p>
            )}
          </section>

          <section className="bg-white/10 backdrop-blur-xl rounded-3xl p-6 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold mb-4">Study Plan</h2>

            <input
              type="text"
              placeholder="Subject e.g. DBMS"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full mb-3 rounded-xl bg-white/10 p-3 outline-none"
            />

            <input
              type="number"
              placeholder="Number of days"
              value={days}
              onChange={(e) => setDays(e.target.value)}
              className="w-full mb-4 rounded-xl bg-white/10 p-3 outline-none"
            />

            <button
              onClick={generatePlan}
              className="w-full rounded-xl bg-purple-500 hover:bg-purple-600 transition p-3 font-semibold"
            >
              Generate Study Plan
            </button>
          </section>

          <section className="bg-white/10 backdrop-blur-xl rounded-3xl p-6 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold mb-4">Ask From Document</h2>

            <textarea
              placeholder="Ask a question from uploaded PDF..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full h-28 mb-4 rounded-xl bg-white/10 p-3 outline-none resize-none"
            />

            <button
              onClick={askQuestion}
              className="w-full rounded-xl bg-emerald-500 hover:bg-emerald-600 transition p-3 font-semibold"
            >
              Ask Question
            </button>
          </section>

          <section className="bg-white/10 backdrop-blur-xl rounded-3xl p-6 shadow-2xl border border-white/10">
            <h2 className="text-2xl font-semibold mb-4">
              MCQs + Flashcards
            </h2>

            <p className="text-slate-300 mb-4">
              This runs the orchestrated agent flow: Summary Agent → MCQ Agent →
              Flashcard Agent.
            </p>

            <button
              onClick={generateMCQ}
              className="w-full rounded-xl bg-pink-500 hover:bg-pink-600 transition p-3 font-semibold"
            >
              Generate MCQs & Flashcards
            </button>
          </section>
        </div>

        <section className="mt-8 bg-black/30 rounded-3xl p-6 border border-white/10 shadow-2xl">
          <h2 className="text-2xl font-semibold mb-4">AI Output</h2>

          {loading && (
            <div className="mb-4 rounded-xl bg-yellow-500/20 text-yellow-300 p-3">
              {loading}
            </div>
          )}

          <pre className="whitespace-pre-wrap text-sm leading-7 text-slate-100 bg-slate-950/70 rounded-2xl p-5 min-h-52 overflow-auto">
            {output || "Your AI output will appear here..."}
          </pre>
        </section>
      </div>
    </main>
  );
}
