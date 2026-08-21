# dao/enrollment_dao.py
"""Data‑access functions for the Enrollment model.
All functions raise ``ValueError`` on missing records so the service layer
can translate them into proper HTTP responses.
"""

from sqlalchemy import func

from config.db import db
from models.course import Course
from models.enrollment import Enrollment
from models.quiz import Quiz
from models.quiz_result import QuizResult

def create_enrollment(user_id, course_id):
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return enrollment

def is_user_enrolled(user_id, course_id):
    return Enrollment.query.filter_by(
        user_id=user_id,
        course_id=course_id
    ).first() is not None

def get_enrollment(enrollment_id):
    return Enrollment.query.get(enrollment_id)

def get_enrollments_by_user(user_id):
    return Enrollment.query.filter_by(user_id=user_id).all()

def count_students_by_instructor(instructor_id):
    return (
        db.session.query(Enrollment.user_id)
        .join(Course, Enrollment.course_id == Course.id)
        .filter(Course.instructor_id == instructor_id)
        .distinct()
        .count()
    )

def get_enrollments_by_course(course_id):
    return Enrollment.query.filter_by(course_id=course_id).all()

def delete_enrollment(user_id, course_id):
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment:
        raise ValueError("Enrollment not found")
    db.session.delete(enrollment)
    db.session.commit()
    return True


