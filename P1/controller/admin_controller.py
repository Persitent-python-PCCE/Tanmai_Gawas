from flask import Blueprint, jsonify
from utils.jwt_util import jwt_required
from utils.role_check import _ensure_admin

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required
def admin_dashboard():
    try:
        _ensure_admin()

        return jsonify({
            'message': 'Admin dashboard placeholder'
        }), 200

    except PermissionError as exc:
        return jsonify({
            'error': str(exc)
        }), 403
