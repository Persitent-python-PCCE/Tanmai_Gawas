# dao/lesson_dao.py
"""DAO for Lesson model."""

from config.db import db
from models.lesson import Lesson

def create_lesson(module_id, title, content='', order=0):
    lesson = Lesson(module_id=module_id, title=title, content=content, order=order)
    db.session.add(lesson)
    db.session.commit()
    return lesson

def get_lesson(lesson_id):
    return Lesson.query.get(lesson_id)

def list_lessons_by_module(module_id):
    return Lesson.query.filter_by(module_id=module_id).all()

def update_lesson(lesson_id, **kwargs):
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise ValueError("Lesson not found")
    for k, v in kwargs.items():
        setattr(lesson, k, v)
    db.session.commit()
    return lesson

def delete_lesson(lesson_id):
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise ValueError("Lesson not found")
    db.session.delete(lesson)
    db.session.commit()
    return True
