# service/lesson_service.py
"""Business logic for lesson management (Phase 2)."""

from dao.lesson_dao import create_lesson, get_lesson, list_lessons_by_module, update_lesson, delete_lesson
from utils.role_check import _ensure_instructor

def create_lesson_service(module_id, data):
    _ensure_instructor()
    return create_lesson(module_id=module_id, **data)

def get_lesson_service(lesson_id):
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise ValueError("Lesson not found")
    return lesson

def list_lessons_service(module_id):
    return list_lessons_by_module(module_id)

def update_lesson_service(lesson_id, data):
    _ensure_instructor()
    return update_lesson(lesson_id, **data)

def delete_lesson_service(lesson_id):
    _ensure_instructor()
    return delete_lesson(lesson_id)
