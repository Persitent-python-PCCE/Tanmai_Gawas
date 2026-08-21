# controller/quiz_controller.py
"""Blueprint exposing quiz management and attempt endpoints.
Routes (all under ``/courses/<course_id>/quizzes``):
* POST   ``/``                – instructor creates a quiz
* GET    ``/``                – list quizzes for a course
* GET    ``/<quiz_id>``       – retrieve quiz metadata (no questions)
* DELETE ``/<quiz_id>``       – instructor deletes a quiz
* POST   ``/<quiz_id>/questions`` – instructor adds a question
* GET    ``/<quiz_id>/questions`` – list questions for a quiz
* DELETE ``/questions/<question_id>`` – instructor deletes a question
* POST   ``/<quiz_id>/attempt`` – student submits answers
* GET    ``/my/results``       – student lists own attempts
* GET    ``/<quiz_id>/results`` – instructor lists attempts for a quiz
"""

from flask import Blueprint, request, jsonify, redirect, url_for, flash
from utils.jwt_util import jwt_required
from service.quiz_service import (
    create_quiz_service,
    list_quizzes_service,
    get_quiz_service,
    delete_quiz_service,
    add_question_service,
    list_questions_service,
    delete_question_service,
    submit_attempt_service,
    get_student_results_service,
    get_quiz_results_service,
)

quiz_bp = Blueprint("quiz", __name__, url_prefix="/courses/<int:course_id>/quizzes")

@quiz_bp.route("/<int:quiz_id>/take", methods=["GET"])
def take_quiz(course_id, quiz_id):
    try:
        quiz = get_quiz_service(quiz_id)
        questions = list_questions_service(quiz_id)
        return render_template("quiz.html", quiz=quiz, questions=questions, course_id=course_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


from flask import render_template

@quiz_bp.route("/view", methods=["GET"])
def view_quizzes(course_id):
    quizzes = list_quizzes_service(course_id)
    return render_template("quiz_list.html", quizzes=quizzes, course_id=course_id)

@quiz_bp.route("/create", methods=["GET", "POST"])
@jwt_required
def create_quiz(course_id):

    if request.method == "GET":
        return render_template(
            "quiz/create_quiz.html",
            course_id=course_id
        )

    try:
        quiz = create_quiz_service(
            course_id,
            request.form
        )
        flash('Quiz created. Add questions next.', 'success')
        return redirect(url_for('quiz.manage_quiz', course_id=course_id, quiz_id=quiz.id))

    except (PermissionError, ValueError) as exc:
        return jsonify({
            "error": str(exc)
        }), 400

@quiz_bp.route("", methods=["GET"])
def list_quizzes(course_id):
    quizzes = list_quizzes_service(course_id)
    payload = [{"id": q.id, "title": q.title} for q in quizzes]
    return jsonify(payload), 200

@quiz_bp.route("/<int:quiz_id>", methods=["GET"])
def get_quiz(course_id, quiz_id):
    try:
        q = get_quiz_service(quiz_id)
        return jsonify({"id": q.id, "title": q.title, "course_id": q.course_id}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

@quiz_bp.route("/<int:quiz_id>", methods=["DELETE"])
def delete_quiz(course_id, quiz_id):
    try:
        delete_quiz_service(quiz_id)
        return jsonify({"message": "Quiz deleted"}), 200
    except (PermissionError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

# ---------- Question ----------
@quiz_bp.route("/<int:quiz_id>/questions", methods=["POST"])
@jwt_required
def add_question(quiz_id, course_id):
    try:
        if request.form:
            options = []
            correct = request.form.get('correct_option')
            for index in range(1, 5):
                text = request.form.get(f'option_{index}')
                if text:
                    options.append({'option': text, 'is_correct': str(index) == correct})
            data = {'prompt': request.form.get('prompt'), 'options': options}
        else:
            data = request.get_json()
        q = add_question_service(quiz_id, data)
        if request.form:
            flash('Question added.', 'success')
            return redirect(url_for('quiz.manage_quiz', course_id=course_id, quiz_id=quiz_id))
        return jsonify({"id": q.id, "prompt": q.prompt}), 201
    except (PermissionError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

@quiz_bp.route("/<int:quiz_id>/questions", methods=["GET"])
def list_questions(quiz_id, course_id):
    qs = list_questions_service(quiz_id)
    payload = [{"id": q.id, "prompt": q.prompt, "options": q.get_options()} for q in qs]
    return jsonify(payload), 200

@quiz_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(course_id, question_id):
    try:
        delete_question_service(question_id)
        return jsonify({"message": "Question deleted"}), 200
    except (PermissionError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

# ---------- Attempt ----------
@quiz_bp.route("/<int:quiz_id>/attempt", methods=["POST"])
@jwt_required
def attempt_quiz(quiz_id, course_id):
    try:
        answers = {}
        if request.form:
            for key, value in request.form.items():
                if key.startswith('q'):
                    answers[key[1:]] = value
        else:
            answers = request.get_json()
        result = submit_attempt_service(quiz_id, answers)
        if request.form:
            flash(f'Quiz submitted. Score: {result.score:.1f}%', 'success')
            return redirect(url_for('progress.my_progress', course_id=course_id))
        return jsonify({"id": result.id, "score": result.score}), 201
    except (PermissionError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

# ---------- Results ----------
@quiz_bp.route("/my/results", methods=["GET"])
@quiz_bp.route("/my/results/view", methods=["GET"])
def view_my_results(course_id):
    results = get_student_results_service()
    return render_template("quiz_results.html", results=results)

    try:
        results = get_student_results_service()
        payload = [
            {
                "quiz_id": r.quiz_id,
                "score": r.score,
                "submitted_at": r.submitted_at.isoformat(),
            }
            for r in results
        ]
        return jsonify(payload), 200
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 401

@quiz_bp.route("/<int:quiz_id>/manage", methods=["GET"])
@jwt_required
def manage_quiz(course_id, quiz_id):
    quiz = get_quiz_service(quiz_id)
    questions = list_questions_service(quiz_id)
    return render_template("quiz/create_quiz.html", course_id=course_id, quiz=quiz, questions=questions)

@quiz_bp.route("/<int:quiz_id>/results", methods=["GET"])
def quiz_results(quiz_id, course_id):
    try:
        res = get_quiz_results_service(quiz_id)
        payload = [
            {
                "student_id": r.student_id,
                "score": r.score,
                "submitted_at": r.submitted_at.isoformat(),
            }
            for r in res
        ]
        return jsonify(payload), 200
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
