import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


@app.get("/")
def home():
    return {"message": "Study Planner Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


async def read_pdf(file: UploadFile):
    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(content)
        temp_path = temp.name

    reader = PdfReader(temp_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


async def generate_study_plan(file: UploadFile):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY missing")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    text = await read_pdf(file)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in PDF")

    prompt = f"""
Create a clear study plan from this document.

Include:
1. Short summary
2. Important topics
3. Day-wise study schedule
4. Revision plan
5. Exam preparation tips

Document:
{text[:12000]}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful study planner assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    return {
        "study_plan": response.choices[0].message.content
    }


@app.post("/generate-plan")
async def generate_plan(file: UploadFile = File(...)):
    return await generate_study_plan(file)


@app.post("/ask")
async def ask(file: UploadFile = File(...)):
    return await generate_study_plan(file)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return await generate_study_plan(file)