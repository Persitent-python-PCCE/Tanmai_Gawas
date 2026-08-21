from flask import Blueprint, render_template, g, redirect, url_for
from service.course_service import list_courses_service
from service.dashboard_service import get_instructor_dashboard_service
from utils.jwt_util import jwt_required
from utils.role_check import _ensure_instructor
from config.db import db
from models.enrollment import Enrollment
from models.user import User
from models.course import Course
from models.quiz import Quiz
from models.quiz_result import QuizResult

instructor_ui_bp = Blueprint('instructor_ui', __name__)

@instructor_ui_bp.route('/instructor', methods=['GET'])
@jwt_required
def dashboard():
    _ensure_instructor()

    user = g.current_user
    instructor_id = int(user['sub'])
    courses, course_count = list_courses_service()

    taught_courses = [c for c in courses if c.instructor_id == instructor_id]
    stats = get_instructor_dashboard_service(instructor_id)

    return render_template(
        'dashboard/instructor_dashboard.html',
        taught_courses=taught_courses,
        user=user,
        stats=stats
    )

@instructor_ui_bp.route('/instructor/courses', methods=['GET'])
@jwt_required
def courses():
    _ensure_instructor()
    user = g.current_user
    instructor_id = int(user['sub'])
    courses, _ = list_courses_service()
    taught_courses = [c for c in courses if c.instructor_id == instructor_id]
    return render_template(
        'dashboard/instructor_courses.html',
        taught_courses=taught_courses,
        user=user
    )

@instructor_ui_bp.route('/instructor/create-course', methods=['GET'])
@jwt_required
def create_course():
    _ensure_instructor()
    return render_template('dashboard/instructor_create_course.html', user=g.current_user)

@instructor_ui_bp.route('/instructor/students', methods=['GET'])
@jwt_required
def students():
    _ensure_instructor()
    user = g.current_user
    instructor_id = int(user['sub'])
    
    # Query students enrolled in this instructor's courses
    enrollments = db.session.query(Enrollment, User, Course).join(
        User, Enrollment.user_id == User.id
    ).join(
        Course, Enrollment.course_id == Course.id
    ).filter(
        Course.instructor_id == instructor_id
    ).all()

    students_data = []
    for enroll, stu, crs in enrollments:
        students_data.append({
            "email": stu.email,
            "course_title": crs.title,
            "enrolled_at": enroll.enrolled_at.strftime('%Y-%m-%d %H:%M')
        })

    return render_template(
        'dashboard/instructor_students.html',
        students_data=students_data,
        user=user
    )

@instructor_ui_bp.route('/instructor/quiz-results', methods=['GET'])
@jwt_required
def quiz_results():
    _ensure_instructor()
    user = g.current_user
    instructor_id = int(user['sub'])

    # Query quiz results for courses taught by this instructor
    results = db.session.query(QuizResult, User, Quiz, Course).join(
        User, QuizResult.student_id == User.id
    ).join(
        Quiz, QuizResult.quiz_id == Quiz.id
    ).join(
        Course, Quiz.course_id == Course.id
    ).filter(
        Course.instructor_id == instructor_id
    ).order_by(QuizResult.submitted_at.desc()).all()

    results_data = []
    for r, stu, q, crs in results:
        results_data.append({
            "student_email": stu.email,
            "quiz_title": q.title,
            "course_title": crs.title,
            "score": int(r.score),
            "submitted_at": r.submitted_at.strftime('%Y-%m-%d %H:%M')
        })

    return render_template(
        'dashboard/instructor_quizzes.html',
        results_data=results_data,
        user=user
    )