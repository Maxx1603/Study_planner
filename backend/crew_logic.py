from crewai import Task, Crew, Process

from agents import (
    topic_agent,
    scheduler_agent,
    summary_agent,
    mcq_agent,
    flashcard_agent,
    doubt_agent
)


def generate_study_plan(subject, days, document_text):
    days = int(days)
    content = document_text[:700]

    topic_task = Task(
        description=f"""
        Extract main topics and subtopics.

        Subject: {subject}

        Document:
        {content}
        """,
        expected_output="Short topic and subtopic list.",
        agent=topic_agent
    )

    schedule_task = Task(
        description=f"""
        Using the extracted topics, create a study schedule for exactly {days} days.

        Include:
        - Day number
        - Topic
        - Break
        - Revision task
        """,
        expected_output=f"Short {days}-day study plan.",
        agent=scheduler_agent,
        context=[topic_task]
    )

    crew = Crew(
        agents=[topic_agent, scheduler_agent],
        tasks=[topic_task, schedule_task],
        process=Process.sequential,
        verbose=True
    )

    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"LLM error: {str(e)}"


def generate_mcq_and_flashcards(document_text):
    content = document_text[:700]

    summary_task = Task(
        description=f"""
        Summarize the important concepts briefly.

        Document:
        {content}
        """,
        expected_output="Short important concepts summary.",
        agent=summary_agent
    )

    mcq_task = Task(
        description="""
        Using the summary from the previous task, generate exactly 3 MCQs.

        STRICT FORMAT:

        Question: ...

        A. ...
        B. ...
        C. ...
        D. ...

        Correct Answer: ...

        Explanation: ...

        Rules:
        - Every question must have exactly 4 options
        - Options must be different
        - Mention only one correct answer
        - Keep explanations short
        """,
        expected_output="""
        3 MCQs with:
        - question
        - 4 options
        - correct answer
        - short explanation
        """,
        agent=mcq_agent,
        context=[summary_task]
    )

    flashcard_task = Task(
        description="""
        Using the generated MCQs, create exactly 3 flashcards.

        STRICT FORMAT:

        Q: ...
        A: ...

        Rules:
        - Flashcards should be short
        - Use concepts from MCQs
        - Do not create multiple-choice options here
        """,
        expected_output="3 flashcards in Q/A format.",
        agent=flashcard_agent,
        context=[mcq_task]
    )

    crew = Crew(
        agents=[summary_agent, mcq_agent, flashcard_agent],
        tasks=[summary_task, mcq_task, flashcard_task],
        process=Process.sequential,
        verbose=True
    )

    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"LLM error: {str(e)}"


def answer_question(question, document_text):
    content = document_text[:1000]

    doubt_task = Task(
        description=f"""
        Answer briefly using only this document.

        Question:
        {question}

        Document:
        {content}
        """,
        expected_output="Brief answer from document.",
        agent=doubt_agent
    )

    crew = Crew(
        agents=[doubt_agent],
        tasks=[doubt_task],
        process=Process.sequential,
        verbose=True
    )

    try:
        return str(crew.kickoff())
    except Exception as e:
        return f"LLM error: {str(e)}"