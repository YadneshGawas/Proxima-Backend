from flask import jsonify
from pydantic import ValidationError
from .registry import ERROR_MAP


def register_error_handlers(app):

    for exc, (status_code, default_msg) in ERROR_MAP.items():

        @app.errorhandler(exc)
        def handle_custom_error(error, status_code=status_code, default_msg=default_msg):
            msg = str(error) or default_msg
            return jsonify({"message": msg}), status_code

    # Validation errors
    @app.errorhandler(ValidationError)
    def handle_pydantic_error(error):
        return jsonify({
            "message": "Invalid data",
            "errors": error.errors()
        }), 400

