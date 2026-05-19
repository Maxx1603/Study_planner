import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

from document_reader import save_and_read_pdf

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is missing")

client = Groq(api_key=GROQ_API_KEY)


@app.get("/")
def home():
    return {"message": "Study Planner Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not GROQ_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY is missing in Render environment variables",
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        text = await save_and_read_pdf(file)

        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        text = text[:12000]

        prompt = f"""
Create a clear study plan from this document.

Include:
1. Short summary
2. Important topics
3. Day-wise study schedule
4. Revision plan
5. Exam preparation tips

Document:
{text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful study planner assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.4,
        )

        return {
            "filename": file.filename,
            "study_plan": response.choices[0].message.content,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))