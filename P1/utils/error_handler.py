# utils/error_handler.py
"""Flask error handling utilities.
Register a generic ``ValueError`` -> 400 JSON response and ``PermissionError`` -> 403.
Any uncaught exception will be turned into a 500 JSON payload (without exposing stack traces).
"""

from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = jsonify({"error": str(error)})
        response.status_code = 400
        return response

    @app.errorhandler(PermissionError)
    def handle_permission_error(error):
        response = jsonify({"error": str(error)})
        response.status_code = 403
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        response = jsonify({"error": "Resource not found"})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def handle_internal_error(error):
        # Do not leak internal details
        response = jsonify({"error": "Internal server error"})
        response.status_code = 500
        return response
