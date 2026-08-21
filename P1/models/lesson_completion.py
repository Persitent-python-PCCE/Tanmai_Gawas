# models/lesson_completion.py

from config.db import db
from datetime import datetime

class LessonCompletion(db.Model):
    __tablename__ = 'lesson_completions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<LessonCompletion s={self.student_id} l={self.lesson_id}>"
