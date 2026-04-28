from http import HTTPStatus
import traceback

from flask import current_app, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from app.exceptions import SkillswapException


def handle_general_exception(error):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    if isinstance(error, HTTPException):
        code = error.code

    response = {
        "code": code,
        "message":
            (str(error)
                if code != HTTPStatus.INTERNAL_SERVER_ERROR
                else "An internal server error occurred."),
    }
    if current_app.debug:
        response["stacktrace"] = traceback.format_exc()

    current_app.logger.error(error, stack_info=True, exc_info=True)
    return response, code


def register_error_handlers(app, login_manager):
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return handle_general_exception(error)
        return render_template(
            "pages/error-404.page.html",
            css_file="/css/pages/error-404.page.css",
            js_file="/js/pages/error-404.page.js",
            main_class='error-404'
        ), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        return handle_general_exception(error)
    
    @app.errorhandler(SkillswapException)
    def handle_validation_exception(error):
        response, _code = handle_general_exception(error)
        response['data'] = error.get_addition_info()
        response['response'] = error.message
        return response, error.code
        

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        if 'private_api' in request.blueprints:
            response = {
                "code": HTTPStatus.UNAUTHORIZED,
                "message": "Unauthorized request"
            }
            return response, HTTPStatus.UNAUTHORIZED
        return redirect(url_for('public.login'))
