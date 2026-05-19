import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

LLM_MODEL = "groq/llama-3.1-8b-instant"


def run_agent(role, goal, backstory, description):
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False,
    )

    task = Task(
        description=description,
        expected_output="Give a clear, useful, structured answer.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)


def planner_agent(text):
    return run_agent(
        role="Study Planner Agent",
        goal="Create a complete study plan from uploaded notes",
        backstory="You are an expert academic planner.",
        description=f"""
Create a study plan from this document.

Include:
1. Summary
2. Important topics
3. Day-wise study plan
4. Revision plan
5. Exam preparation tips

Document:
{text[:12000]}
""",
    )


def qa_agent(text, question):
    return run_agent(
        role="Question Answering Agent",
        goal="Answer student questions using the uploaded document",
        backstory="You answer only from the document content.",
        description=f"""
Answer this question using the document.

Question:
{question}

Document:
{text[:12000]}
""",
    )


def schedule_agent(text, days):
    return run_agent(
        role="Schedule Agent",
        goal="Create a study schedule based on available days",
        backstory="You create practical timetables for students.",
        description=f"""
Create a {days}-day study schedule from this document.

Document:
{text[:12000]}
""",
    )


def flashcard_agent(text):
    return run_agent(
        role="Flashcard Agent",
        goal="Create flashcards for revision",
        backstory="You create exam-focused flashcards.",
        description=f"""
Create flashcards from this document.

Format:
Q:
A:

Document:
{text[:12000]}
""",
    )