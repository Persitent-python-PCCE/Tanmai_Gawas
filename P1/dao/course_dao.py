# dao/course_dao.py
"""Data‑access layer for Course model."""

from config.db import db
from models.course import Course
from models.user import User

def create_course(title, description, instructor_id):
    course = Course(title=title, description=description, instructor_id=instructor_id)
    db.session.add(course)
    db.session.commit()
    return course

def get_course(course_id):
    return Course.query.get(course_id)

from sqlalchemy import or_


def list_courses(search=None, page=1, per_page=10):
    """
    Returns (courses, total_count) for the given page, optionally filtered
    by a case-insensitive match against course title or instructor email.
    """
    query = Course.query

    if search:
        like_pattern = f"%{search}%"
        query = query.join(User, Course.instructor_id == User.id).filter(
            or_(
                Course.title.ilike(like_pattern),
                User.email.ilike(like_pattern)
            )
        )

    total = query.count()

    courses = (
        query.order_by(Course.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return courses, total

def update_course(course_id, **kwargs):
    course = get_course(course_id)
    if not course:
        raise ValueError("Course not found")
    for key, value in kwargs.items():
        setattr(course, key, value)
    db.session.commit()
    return course

def delete_course(course_id):
    course = get_course(course_id)
    if not course:
        raise ValueError("Course not found")
    db.session.delete(course)
    db.session.commit()
    return True

