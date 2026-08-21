# service/quiz_service.py
"""Service layer for quiz CRUD, question management, and quiz attempts.
* Instructors can create/update/delete quizzes and questions.
* Students can retrieve a quiz (questions only) and submit their answers.
* Scoring is simple: count correct options vs total.
"""

from dao.quiz_dao import (
    average_score_by_instructor,
    count_quizzes_by_instructor,
    create_quiz,
    get_quiz,
    list_quizzes_by_course,
    delete_quiz,
    create_question,
    get_question,
    list_questions_by_quiz,
    delete_question,
    submit_quiz_result,
    list_results_by_student,
    list_results_by_quiz,
)
from utils.role_check import _ensure_instructor, _ensure_student, get_current_user_id

# ---------- Quiz CRUD ----------
def create_quiz_service(course_id, data):
    _ensure_instructor()
    title = data.get("title")
    if not title:
        raise ValueError("Quiz title required")
    return create_quiz(title, course_id, instructor_id=get_current_user_id())

def get_quiz_service(quiz_id):
    quiz = get_quiz(quiz_id)
    if not quiz:
        raise ValueError("Quiz not found")
    return quiz

def list_quizzes_service(course_id):
    return list_quizzes_by_course(course_id)


def delete_quiz_service(quiz_id):
    _ensure_instructor()
    return delete_quiz(quiz_id)

# ---------- Question CRUD ----------
def add_question_service(quiz_id, data):
    _ensure_instructor()
    prompt = data.get("prompt")
    options = data.get("options")  # expects list of {"option": ..., "is_correct": bool}
    if not prompt or not isinstance(options, list) or not options:
        raise ValueError("Prompt and non‑empty options list required")
    return create_question(quiz_id, prompt, options)

def list_questions_service(quiz_id):
    return list_questions_by_quiz(quiz_id)

def delete_question_service(question_id):
    _ensure_instructor()
    return delete_question(question_id)

# ---------- Student attempt ----------
def submit_attempt_service(quiz_id, answers_dict):
    _ensure_student()
    # answers_dict: {question_id: chosen_index}
    questions = list_questions_by_quiz(quiz_id)
    if not questions:
        raise ValueError("Quiz has no questions")
    # Compute score
    total = len(questions)
    correct = 0
    for q in questions:
        chosen = answers_dict.get(str(q.id))  # keys may be strings from JSON payload
        opts = q.get_options()
        # Find the correct option index
        correct_idx = next((i for i, o in enumerate(opts) if o.get("is_correct")), None)
        if chosen is not None and int(chosen) == correct_idx:
            correct += 1
    score = correct / total * 100  # percentage
    return submit_quiz_result(quiz_id, student_id=get_current_user_id(), answers_dict=answers_dict, score=score)

def get_student_results_service():
    _ensure_student()
    return list_results_by_student(get_current_user_id())

def get_quiz_results_service(quiz_id):
    _ensure_instructor()
    return list_results_by_quiz(quiz_id)

def get_instructor_quiz_stats_service(instructor_id):
    _ensure_instructor()

    return {
        "total_quizzes": count_quizzes_by_instructor(instructor_id),
        "average_score": average_score_by_instructor(instructor_id)
    }
