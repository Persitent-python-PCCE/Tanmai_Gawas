# service/module_service.py
"""Business logic for module management (Phase 2)."""

from dao.module_dao import create_module, get_module, list_modules_by_course, update_module, delete_module
from utils.role_check import _ensure_instructor

def create_module_service(course_id, data):
    _ensure_instructor()
    filtered = {k: v for k, v in data.items() if k in ('title', 'order')}
    return create_module(course_id=course_id, **filtered)

def get_module_service(module_id):
    module = get_module(module_id)
    if not module:
        raise ValueError("Module not found")
    return module

def list_modules_service(course_id):
    return list_modules_by_course(course_id)

def update_module_service(module_id, data):
    _ensure_instructor()
    return update_module(module_id, **data)

def delete_module_service(module_id):
    _ensure_instructor()
    return delete_module(module_id)
