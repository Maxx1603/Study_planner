import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")


def run_agent_task(role, goal, backstory, task_description):
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm="groq/llama-3.1-8b-instant",
        verbose=True,
        allow_delegation=False,
    )

    task = Task(
        description=task_description,
        expected_output="Clear, structured, useful output for a student.",
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
    return run_agent_task(
        role="Study Planner Agent",
        goal="Create a useful study plan from academic content",
        backstory="You are an expert academic planner who creates practical study plans.",
        task_description=f"""
Create a study plan from this document.

Include:
1. Summary
2. Important topics
3. Day-wise plan
4. Revision plan
5. Exam tips

Document:
{text[:12000]}
""",
    )


def qa_agent(text, question):
    return run_agent_task(
        role="Question Answering Agent",
        goal="Answer student questions using only the uploaded document",
        backstory="You are a document Q&A expert.",
        task_description=f"""
Answer this question using the document.

Question:
{question}

Document:
{text[:12000]}
""",
    )


def schedule_agent(text, days):
    return run_agent_task(
        role="Schedule Agent",
        goal="Create a study timetable based on available days",
        backstory="You are an expert timetable planner.",
        task_description=f"""
Create a {days}-day study schedule from this document.

Document:
{text[:12000]}
""",
    )


def flashcard_agent(text):
    return run_agent_task(
        role="Flashcard Agent",
        goal="Create useful flashcards for revision",
        backstory="You create exam-focused flashcards.",
        task_description=f"""
Create flashcards from this document.

Format:
Q: question
A: answer

Document:
{text[:12000]}
""",
    )