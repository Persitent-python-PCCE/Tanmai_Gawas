# dao/quiz_dao.py
"""DAO layer for Quiz, Question and QuizResult.
All functions raise ``ValueError`` on missing records for the service layer to handle.
"""

from sqlalchemy import func

from config.db import db
from models.quiz import Quiz
from models.question import Question
from models.quiz_result import QuizResult
import json

# ---------- Quiz ----------

def create_quiz(title, course_id, instructor_id):
    quiz = Quiz(title=title, course_id=course_id, instructor_id=instructor_id)
    db.session.add(quiz)
    db.session.commit()
    return quiz

def get_quiz(quiz_id):
    return Quiz.query.get(quiz_id)

def list_quizzes_by_course(course_id):
    return Quiz.query.filter_by(course_id=course_id).all()

def delete_quiz(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        raise ValueError("Quiz not found")
    db.session.delete(quiz)
    db.session.commit()
    return True

# ---------- Question ----------

def create_question(quiz_id, prompt, options):
    q = Question(prompt=prompt, quiz_id=quiz_id)
    q.set_options(options)
    db.session.add(q)
    db.session.commit()
    return q

def get_question(question_id):
    return Question.query.get(question_id)

def list_questions_by_quiz(quiz_id):
    return Question.query.filter_by(quiz_id=quiz_id).all()

def delete_question(question_id):
    q = get_question(question_id)
    if not q:
        raise ValueError("Question not found")
    db.session.delete(q)
    db.session.commit()
    return True

# ---------- QuizResult ----------

def submit_quiz_result(quiz_id, student_id, answers_dict, score):
    result = QuizResult(
        quiz_id=quiz_id,
        student_id=student_id,
        score=score,
    )
    result.set_answers(answers_dict)
    db.session.add(result)
    db.session.commit()
    return result

def get_quiz_result(result_id):
    return QuizResult.query.get(result_id)

def list_results_by_quiz(quiz_id):
    return QuizResult.query.filter_by(quiz_id=quiz_id).all()

def list_results_by_student(student_id):
    return QuizResult.query.filter_by(student_id=student_id).all()

def get_quiz_results_by_student_and_course(student_id: int, course_id: int):
    """Return all QuizResult objects for a student in a specific course."""
    # Join QuizResult -> Quiz to filter by course_id
    return (
        QuizResult.query.join(Quiz, QuizResult.quiz_id == Quiz.id)
        .filter(QuizResult.student_id == student_id, Quiz.course_id == course_id)
        .all()
    )

def count_quizzes_by_instructor(instructor_id):
    return Quiz.query.filter_by(
        instructor_id=instructor_id
    ).count()

def average_score_by_instructor(instructor_id):
    result = (
        db.session.query(func.avg(QuizResult.score))
        .join(Quiz, QuizResult.quiz_id == Quiz.id)
        .filter(Quiz.instructor_id == instructor_id)
        .scalar()
    )

    return round(float(result), 2) if result is not None else 0.0

