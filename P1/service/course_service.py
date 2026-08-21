# service/course_service.py
"""Business logic for course management (Phase 2)."""

from dao.course_dao import create_course, get_course, list_courses, update_course, delete_course
from service.enrollment_service import _ensure_instructor_or_admin
from utils.role_check import _ensure_admin, _ensure_instructor, get_current_user_id

def create_course_service(data):
    _ensure_instructor_or_admin()
    if data.get('instructor_id') is not None:
        instructor_id = data.get('instructor_id')
    else:
        instructor_id = get_current_user_id()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        raise ValueError("Course title required")
    return create_course(title=title, description=description, instructor_id=instructor_id)

# def create_course_admin_service(data):
#     _ensure_admin()
#     instructor_id = data.get('instructor_id')
#     title = data.get('title')
#     description = data.get('description', '')
    
#     if not title:
#         raise ValueError("Course title required")
#     return create_course(title=title, description=description, instructor_id=instructor_id)



def get_course_service(course_id):
    course = get_course(course_id)
    if not course:
        raise ValueError("Course not found")
    return course

def list_courses_service(search=None, page=1, per_page=10):
    return list_courses(search, page, per_page)

def update_course_service(course_id, data):
    _ensure_instructor()
    return update_course(course_id, **data)

def delete_course_service(course_id):
    _ensure_instructor()
    return delete_course(course_id)

def admin_update_course_service(course_id, data):
    return update_course(
        course_id,
        **data
    )

def list_courses_by_instructor(instructor_id):
    _ensure_instructor_or_admin()
    courses, count = list_courses_service()
    return [c for c in courses if c.instructor_id == instructor_id]

