# service/material_service.py
"""Business logic for material handling (Phase 4)."""

from dao.material_dao import create_material, get_material, list_materials_by_module, delete_material
from utils.role_check import _ensure_instructor, get_current_user_id
from utils.file_validation import allowed_file, validate_file_size

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'mp4', 'doc', 'docx'}
MAX_SIZE_MB = 50

def upload_material_service(module_id, file_storage):
    _ensure_instructor()
    filename = file_storage.filename
    if not allowed_file(filename, ALLOWED_EXTENSIONS):
        raise ValueError("Invalid file extension")
    if not validate_file_size(file_storage, MAX_SIZE_MB):
        raise ValueError("File exceeds size limit")
    # Save file to uploads/<course_id>/<module_id>/
    from werkzeug.utils import secure_filename
    import os
    secure_name = secure_filename(filename)
    upload_dir = os.path.join('uploads', str(module_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, secure_name)
    file_storage.save(file_path)
    return create_material(module_id=module_id, file_path=file_path, file_type=secure_name.rsplit('.',1)[-1], uploaded_by=get_current_user_id())

def list_materials_service(module_id):
    return list_materials_by_module(module_id)

def delete_material_service(material_id):
    _ensure_instructor()
    return delete_material(material_id)
