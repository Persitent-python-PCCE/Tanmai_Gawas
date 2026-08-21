# service/enrollment_service.py
"""Business logic for enrollment actions.
* Students may enroll or unenroll from a course.
* Instructors and admins may list enrollments for a course.
* All operations enforce role checks via ``utils.role_check`` helpers.
"""

from dao.enrollment_dao import (
    count_students_by_instructor,
    create_enrollment,
    get_enrollments_by_user,
    get_enrollments_by_course,
    delete_enrollment,
)
from flask_login import current_user
from flask import g
from utils.role_check import _ensure_student, get_current_user_id

from dao.enrollment_dao import is_user_enrolled

def is_user_enrolled_service(user_id: int, course_id: int) -> bool:
    return is_user_enrolled(user_id, course_id)

def _ensure_instructor_or_admin():
    jwt_user = getattr(g, 'current_user', None)
    if jwt_user:
        if jwt_user.get('role') not in {"instructor", "admin"}:
            raise PermissionError("Only instructors or admins may view enrollments (JWT)")
        return
    if not current_user.is_authenticated:
        raise PermissionError("Authentication required")
    if getattr(current_user, "role", None) not in {"instructor", "admin"}:
        raise PermissionError("Only instructors or admins may view enrollments")

def enroll_student(course_id):
    _ensure_student()
    return create_enrollment(user_id=get_current_user_id(), course_id=course_id)

def unenroll_student(course_id):
    _ensure_student()
    return delete_enrollment(user_id=get_current_user_id(), course_id=course_id)

def list_my_enrollments():
    student_id = get_current_user_id()
    print(student_id)
    if not student_id:
        raise PermissionError("Authentication required")
    courses = get_enrollments_by_user(student_id)
    print("courses:",[c.to_dict() for c in courses])
    return courses

def list_course_enrollments(course_id):
    _ensure_instructor_or_admin()
    return get_enrollments_by_course(course_id)

def count_students_by_instructor_service(instructor_id):
    _ensure_instructor_or_admin()
    return count_students_by_instructor(instructor_id)