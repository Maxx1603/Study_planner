from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from document_reader import save_and_read_pdf
from crew_logic import generate_study_plan, answer_question, generate_mcq_and_flashcards

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_text = ""


@app.get("/")
def home():
    return {"message": "AI Study Planner Backend is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global document_text
    document_text = await save_and_read_pdf(file)

    return {
        "message": "PDF uploaded successfully",
        "characters_extracted": len(document_text)
    }


@app.post("/generate-plan")
def create_plan(subject: str = Form(...), days: int = Form(...)):
    if not document_text:
        return {"error": "Please upload a PDF first"}

    result = generate_study_plan(subject, days, document_text)
    return {"result": result}


@app.post("/ask")
def ask_question_api(question: str = Form(...)):
    if not document_text:
        return {"error": "Please upload a PDF first"}

    result = answer_question(question, document_text)
    return {"answer": result}


@app.post("/generate-mcq")
def create_mcq():
    if not document_text:
        return {"error": "Please upload a PDF first"}

    result = generate_mcq_and_flashcards(document_text)
    return {"result": result}