import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

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
        expected_output="Give a clear, useful and structured answer.",
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
        "Study Planner Agent",
        "Create a complete study plan from uploaded notes",
        "You are an expert academic planner.",
        f"""
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
        "Question Answering Agent",
        "Answer questions using the uploaded document",
        "You answer only from the document content.",
        f"""
Question:
{question}

Document:
{text[:12000]}
""",
    )


def schedule_agent(text, days):
    return run_agent(
        "Schedule Agent",
        "Create a study schedule based on available days",
        "You create practical timetables for students.",
        f"""
Create a {days}-day study schedule from this document.

Document:
{text[:12000]}
""",
    )


def flashcard_agent(text):
    return run_agent(
        "Flashcard Agent",
        "Create flashcards for revision",
        "You create exam-focused flashcards.",
        f"""
Create flashcards from this document.

Format:
Q:
A:

Document:
{text[:12000]}
""",
    )