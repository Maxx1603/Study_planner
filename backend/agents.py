import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

topic_agent = Agent(
    role="Topic Breakdown Agent",
    goal="Break study material into topics and subtopics",
    backstory="You are an expert teacher who explains subjects simply.",
    llm=llm,
    verbose=True
)

scheduler_agent = Agent(
    role="Study Scheduler Agent",
    goal="Create day-wise study timetable using extracted topics",
    backstory="You create realistic study schedules for students.",
    llm=llm,
    verbose=True
)

summary_agent = Agent(
    role="Summary Agent",
    goal="Create a short summary from uploaded study material",
    backstory="You extract only the most important concepts.",
    llm=llm,
    verbose=True
)

mcq_agent = Agent(
    role="MCQ Agent",
    goal="Create MCQs from summarized notes",
    backstory="You create simple exam-style MCQs.",
    llm=llm,
    verbose=True
)

flashcard_agent = Agent(
    role="Flashcard Agent",
    goal="Create flashcards from generated MCQs",
    backstory="You convert MCQs into quick revision flashcards.",
    llm=llm,
    verbose=True
)

doubt_agent = Agent(
    role="Doubt Solver Agent",
    goal="Answer student doubts from uploaded document",
    backstory="You answer only from uploaded study material.",
    llm=llm,
    verbose=True
)