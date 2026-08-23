from flask import Blueprint, render_template, redirect, url_for, flash, request
from utils.jwt_util import jwt_required
from utils.role_check import _ensure_student
from service.enrollment_service import enroll_student, unenroll_student, list_my_enrollments

enroll_ui_bp = Blueprint('enroll_ui', __name__)

@enroll_ui_bp.route('/my/enrollments', methods=['GET'])
@jwt_required
def my_enrollments():
    _ensure_student()
    enrollments = list_my_enrollments()
    return render_template('enrollment/my_enrollments.html', enrollments=enrollments, courses=[e.course for e in enrollments])

@enroll_ui_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required
def enroll(course_id):
    _ensure_student()
    enroll_student(course_id)
    flash('Enrolled successfully', 'success')
    return redirect(url_for('course.course_detail', course_id=course_id))

@enroll_ui_bp.route('/courses/<int:course_id>/unenroll', methods=['POST'])
@jwt_required
def unenroll(course_id):
    _ensure_student()
    unenroll_student(course_id)
    flash('Unenrolled successfully', 'info')
    return redirect(url_for('enroll_ui.my_enrollments', course_id=course_id))
