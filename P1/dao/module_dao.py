# dao/module_dao.py
"""DAO for Module model."""

from config.db import db
from models.module import Module

def create_module(course_id, title, order=0):
    module = Module(course_id=course_id, title=title, order=order)
    db.session.add(module)
    db.session.commit()
    return module

def get_module(module_id):
    return Module.query.get(module_id)

def list_modules_by_course(course_id):
    return Module.query.filter_by(course_id=course_id).all()

def update_module(module_id, **kwargs):
    module = get_module(module_id)
    if not module:
        raise ValueError("Module not found")
    for k, v in kwargs.items():
        setattr(module, k, v)
    db.session.commit()
    return module

def delete_module(module_id):
    module = get_module(module_id)
    if not module:
        raise ValueError("Module not found")
    db.session.delete(module)
    db.session.commit()
    return True
