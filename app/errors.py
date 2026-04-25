import traceback

from flask import current_app, redirect, request, url_for
from werkzeug.exceptions import HTTPException


def handle_general_exception(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code

    response = {
        "code": code,
        "message": str(error) if code != 500 else "An internal server error occurred.",
    }
    if current_app.debug:
        response["stacktrace"] = traceback.format_exc()

    current_app.logger.error(error, stack_info=True, exc_info=True)
    return response, code


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/") or request.accept_mimetypes.accept_json:
            return handle_general_exception(error)
        return redirect(url_for("views.index", _anchor=404))

    @app.errorhandler(Exception)
    def handle_exception(error):
        return handle_general_exception(error)