from crewai import Task
from backend.agents import notes_agent, quiz_agent, flashcard_agent, plan_agent


def create_material_tasks(text):
    notes_task = Task(
        description=f"Create clear structured notes from this text:\n{text}",
        expected_output="Well formatted bullet point notes",
        agent=notes_agent
    )

    quiz_task = Task(
        description=f"Generate 5-10 multiple-choice questions from this text, including answer keys:\n{text}",
        expected_output="MCQs with options and correct answers",
        agent=quiz_agent
    )

    flashcard_task = Task(
        description=f"Convert this text into study flashcards with question-and-answer pairs:\n{text}",
        expected_output="Q&A flashcards format",
        agent=flashcard_agent
    )

    return [notes_task, quiz_task, flashcard_task]


def create_study_plan_task(topic, deadline, hours_per_day=2, learning_style=None):
    prompt = (
        f"Create a practical study plan for this topic: {topic}. "
        f"The deadline is {deadline}. "
        f"Assume the learner has {hours_per_day} hours available each day. "
    )

    if learning_style:
        prompt += f"The learner prefers {learning_style} learning. "

    prompt += "Include milestones, daily tasks, and review recommendations."

    return [
        Task(
            description=prompt,
            expected_output="Structured study schedule with milestones and daily/weekly planning",
            agent=plan_agent
        )
    ]
