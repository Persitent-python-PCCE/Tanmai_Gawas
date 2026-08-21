from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from service.course_service import get_course_service
from utils.jwt_util import jwt_required
from service.module_service import (
    create_module_service,
    get_module_service,
    list_modules_service,
    update_module_service,
    delete_module_service,
)

module_bp = Blueprint('module', __name__, url_prefix='/courses/<int:course_id>/modules')

@module_bp.route('', methods=['POST'])
@jwt_required
def create_module(course_id):
    try:
        data = request.form if request.form else request.get_json()
        m = create_module_service(course_id, data)
        if request.form:
            flash('Module created.', 'success')
            return redirect(url_for('course.course_detail', course_id=course_id))
        return jsonify({'id': m.id, 'title': getattr(m, 'title', None)}), 201
    except (PermissionError, ValueError) as exc:
        return jsonify({'error': str(exc)}), 400

@module_bp.route('/create-module', methods=['GET'])
@jwt_required
def module_form(course_id):
    course=get_course_service(course_id)

    return render_template(
        'course/module_form.html',
        course_id=course_id,
        course=course
    )

@module_bp.route('', methods=['GET'])
def list_modules(course_id):
    modules = list_modules_service(course_id)
    payload = [{'id': m.id, 'title': getattr(m, 'title', None)} for m in modules]
    return jsonify(payload), 200

@module_bp.route('/<int:module_id>', methods=['GET'])
def get_module(course_id, module_id):
    try:
        m = get_module_service(module_id)
        return jsonify({'id': m.id, 'title': getattr(m, 'title', None)}), 200
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 404

@module_bp.route('/<int:module_id>', methods=['PUT'])
@jwt_required
def update_module(course_id, module_id):
    try:
        m = update_module_service(module_id, request.get_json())
        return jsonify({'id': m.id, 'title': getattr(m, 'title', None)}), 200
    except (PermissionError, ValueError) as exc:
        return jsonify({'error': str(exc)}), 400

@module_bp.route('/<int:module_id>', methods=['DELETE'])
@jwt_required
def delete_module(course_id, module_id):
    try:
        delete_module_service(module_id)
        return jsonify({'message': 'Module deleted'}), 200
    except PermissionError as exc:
        return jsonify({'error': str(exc)}), 403
