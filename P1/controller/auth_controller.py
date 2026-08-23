# controller/auth_controller.py

from flask import Blueprint, flash, make_response, redirect, request, jsonify, session, render_template, url_for
from service.auth_service import register_user, authenticate_user, logout_user
from flask_login import login_user, logout_user as flask_logout, login_required, current_user

from utils.jwt_util import create_access_token
from utils.logger import log_general_action

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST','GET'])
@auth_bp.route('/auth/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    data = request.get_json(silent=True) or request.form
    is_json = request.is_json or (request.get_json(silent=True) is not None)
    try:
        user, msg = register_user(data)
        if is_json:
            return jsonify({'message': msg}), 201
        flash(f'{msg}. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    except ValueError as exc:
        if is_json:
            return jsonify({'error': str(exc)}), 400
        flash(str(exc), 'error')
        return redirect(url_for('auth.register'))

@auth_bp.route('/login', methods=['GET','POST'])
@auth_bp.route('/auth/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    data = request.form if request.form else request.get_json()
    user = authenticate_user(data)
    if user:
        login_user(user)
        from utils.jwt_util import create_access_token
        token = create_access_token(
            user_id=user.id,
            role=user.role,
            email=user.email
        )
        log_general_action(f"[OK] User Logged In Successfully with email {user.email}", "info")
        response = make_response(jsonify({'message': 'Logged in', 'token': token}))
        response.set_cookie(
            'access_token',
            token,
            httponly=True,
            secure=False,       # True when using HTTPS
            samesite='Lax'
        )
        return response, 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/login_jwt', methods=['GET', 'POST'])
@auth_bp.route('/auth/login_jwt', methods=['GET', 'POST'])
def login_jwt():

    if request.method == 'GET':
        return render_template('auth/login.html')

    data = request.get_json(silent=True) or request.form
    is_json = request.is_json or (request.get_json(silent=True) is not None)

    user = authenticate_user(data)

    if not user:
        return jsonify({
            'error': 'Invalid credentials'
        }), 401


    token = create_access_token(
        user_id=user.id,
        role=user.role,
        email=user.email
    )

    if is_json:
        return jsonify({'token': token}), 200

    response = make_response(
        redirect(url_for('dashboard.home'))
    )

    response.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=False,
        samesite='Lax'
    )

    return response


@auth_bp.route('/logout', methods=['POST'])
@auth_bp.route('/auth/logout', methods=['POST'])
def logout():

    response = make_response(redirect(url_for('auth.login_jwt')))

    response.delete_cookie('access_token')

    return response
