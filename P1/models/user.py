# models/user.py

from config.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            "id":self.id,
            "email":self.email,
            "role":self.role,
            "created_at":self.created_at
        }
