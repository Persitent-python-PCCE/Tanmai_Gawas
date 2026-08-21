# dao/material_dao.py
"""DAO for Material model."""

from config.db import db
from models.material import Material

def create_material(module_id, file_path, file_type, uploaded_by):
    material = Material(module_id=module_id, file_path=file_path, file_type=file_type, uploaded_by=uploaded_by)
    db.session.add(material)
    db.session.commit()
    return material

def get_material(material_id):
    return Material.query.get(material_id)

def list_materials_by_module(module_id):
    return Material.query.filter_by(module_id=module_id).all()

def delete_material(material_id):
    material = get_material(material_id)
    if not material:
        raise ValueError("Material not found")
    db.session.delete(material)
    db.session.commit()
    return True
