# Study Planner

A CrewAI-backed multi-agent study planner.

## Backend

- `backend/main.py` - FastAPI server with PDF upload, study plan generation, and doubt answering.
- `backend/agents.py` - CrewAI agents for notes, quizzes, flashcards, study plans, and doubt solving.
- `backend/tasks.py` - Task builders for material processing and study planning.

## Run locally

1. Create a Python virtual environment.
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Start the API: `uvicorn backend.main:app --reload`

## API endpoints

- `POST /upload-pdf/` - upload a PDF to generate notes, quizzes, and flashcards.
- `POST /create-study-plan/` - build a study schedule for a topic and deadline.
- `POST /ask-doubt/` - answer a student question.

## Notes

- Configure CrewAI credentials as required by the `crewai` package.
- The study plan agent currently uses a single task to generate a schedule from the topic and deadline.
