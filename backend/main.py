import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pypdf import PdfReader

from agents import planner_agent, qa_agent, schedule_agent, flashcard_agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Study Planner Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


async def extract_pdf_text(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(content)
        temp_path = temp.name

    text = ""

    try:
        reader = PdfReader(temp_path)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in PDF")

    return text


@app.post("/generate-plan")
async def generate_plan(file: UploadFile = File(...)):
    text = await extract_pdf_text(file)
    result = planner_agent(text)
    return {"study_plan": result}


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...),
):
    text = await extract_pdf_text(file)
    result = qa_agent(text, question)
    return {"answer": result}


@app.post("/generate-schedule")
async def generate_schedule(
    file: UploadFile = File(...),
    days: int = Form(...),
):
    text = await extract_pdf_text(file)
    result = schedule_agent(text, days)
    return {"schedule": result}


@app.post("/generate-flashcards")
async def generate_flashcards(file: UploadFile = File(...)):
    text = await extract_pdf_text(file)
    result = flashcard_agent(text)
    return {"flashcards": result}