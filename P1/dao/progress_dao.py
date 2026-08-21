# dao/progress_dao.py
"""DAO for Progress model."""

from config.db import db
from models.progress import Progress

def get_progress(student_id, course_id):
    return Progress.query.filter_by(student_id=student_id, course_id=course_id).first()

def update_progress(student_id, course_id, completion_percent):
    prog = get_progress(student_id, course_id)
    if not prog:
        prog = Progress(student_id=student_id, course_id=course_id, completion_percent=completion_percent)
        db.session.add(prog)
    else:
        prog.completion_percent = completion_percent
    db.session.commit()
    return prog
