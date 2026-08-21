# dao/analytics_dao.py

from sqlalchemy import func, case

from models.course import Course
from models.enrollment import Enrollment
from models.quiz import Quiz
from models.quiz_result import QuizResult

from config.db import db

def get_course_performance(instructor_id):

    results = (
        db.session.query(
            Course.id,
            Course.title,

            func.count(
                func.distinct(Enrollment.user_id)
            ).label("student_count"),

            func.avg(
                QuizResult.score
            ).label("avg_score")
        )
        .outerjoin(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .outerjoin(
            Quiz,
            Quiz.course_id == Course.id
        )
        .outerjoin(
            QuizResult,
            QuizResult.quiz_id == Quiz.id
        )
        .filter(
            Course.instructor_id == instructor_id
        )
        .group_by(
            Course.id,
            Course.title
        )
        .all()
    )

    return results

def get_quiz_performance(instructor_id):

    results = (
        db.session.query(
            Quiz.id,
            Quiz.title,

            func.count(
                QuizResult.id
            ).label("attempts"),

            func.avg(
                QuizResult.score
            ).label("avg_score"),

            (
                func.sum(
                    case(
                        (QuizResult.score >= 40, 1),
                        else_=0
                    )
                ) * 100.0
                /
                func.nullif(
                    func.count(QuizResult.id),
                    0
                )
            ).label("pass_rate")
        )
        .join(
            Course,
            Course.id == Quiz.course_id
        )
        .outerjoin(
            QuizResult,
            QuizResult.quiz_id == Quiz.id
        )
        .filter(
            Course.instructor_id == instructor_id
        )
        .group_by(
            Quiz.id,
            Quiz.title
        )
        .all()
    )

    return results