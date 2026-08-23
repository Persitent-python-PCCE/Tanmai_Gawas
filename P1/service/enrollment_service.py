# service/enrollment_service.py
"""Business logic for enrollment actions (Phase 3)."""

from dao.enrollment_dao import (
    create_enrollment,
    is_user_enrolled,
    get_enrollments_by_user,
    get_enrollments_by_course,
    count_students_by_instructor,
    delete_enrollment,
)
from utils.role_check import _ensure_student, _ensure_instructor, _ensure_admin, get_current_user_id


def _ensure_instructor_or_admin():
    """Utility to ensure the current user is either an instructor or admin.
    Works for both JWT and Flask-Login contexts.
    """
    try:
        _ensure_instructor()
    except PermissionError:
        _ensure_admin()


def _ensure_instructor_or_admin_for_course():
    """Utility to ensure the current user is instructor or admin for course operations."""
    try:
        _ensure_instructor()
    except PermissionError:
        _ensure_admin()


class EnrollmentService:
    """Encapsulates enrollment operations."""

    def is_user_enrolled(self, user_id: int, course_id: int) -> bool:
        return is_user_enrolled(user_id, course_id)

    def enroll_student(self, course_id):
        _ensure_student()
        from dao.course_dao import get_course
        course = get_course(course_id)
        if not course:
            raise ValueError("Course not found")
        return create_enrollment(user_id=get_current_user_id(), course_id=course_id)

    def unenroll_student(self, course_id):
        _ensure_student()
        return delete_enrollment(user_id=get_current_user_id(), course_id=course_id)

    def list_my_enrollments(self):
        student_id = get_current_user_id()
        if not student_id:
            raise PermissionError("Authentication required")
        return get_enrollments_by_user(student_id)

    def list_course_enrollments(self, course_id):
        _ensure_instructor_or_admin_for_course()
        return get_enrollments_by_course(course_id)

    def count_students_by_instructor(self, instructor_id):
        _ensure_instructor()
        return count_students_by_instructor(instructor_id)


# Module‑level singleton
enrollment_service = EnrollmentService()

# Backward‑compatible wrappers
def is_user_enrolled_service(*args, **kwargs):
    return enrollment_service.is_user_enrolled(*args, **kwargs)

def enroll_student(*args, **kwargs):
    return enrollment_service.enroll_student(*args, **kwargs)

def unenroll_student(*args, **kwargs):
    return enrollment_service.unenroll_student(*args, **kwargs)

def list_my_enrollments(*args, **kwargs):
    return enrollment_service.list_my_enrollments(*args, **kwargs)

def list_course_enrollments(*args, **kwargs):
    return enrollment_service.list_course_enrollments(*args, **kwargs)

def count_students_by_instructor_service(*args, **kwargs):
    return enrollment_service.count_students_by_instructor(*args, **kwargs)