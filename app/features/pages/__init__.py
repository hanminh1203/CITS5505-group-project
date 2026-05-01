from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, logout_user, current_user

from app.features.requests.views import requests_views_bp
from app.forms.login import LoginForm


def render_template_with_class(
    page,
    has_css=True,
    has_js=True,
    **addition_variables,
):
    return render_template(
        f"pages/{page}.page.html",
        css_file=f"/css/pages/{page}.page.css" if has_css else None,
        js_file=f"/js/pages/{page}.page.js" if has_js else None,
        main_class=page,
        **addition_variables
    )


def render_fragment(section, name, **kwargs):
    return render_template(f"{section}/{name}.{section[:-1]}.html", **kwargs)


def create_public_views_blueprint():
    public_views_bp = Blueprint("public", __name__, url_prefix="/")

    @public_views_bp.route("/", methods=['GET'])
    @public_views_bp.route("/index.html", methods=['GET'])
    def index():
        return render_template_with_class("home")

    @public_views_bp.route("/login", methods=['GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('private.dashboard'))
        return render_template_with_class('login', form=LoginForm())

    @public_views_bp.route("/register", methods=['GET'])
    def register():
        return render_template_with_class("login", has_js=False)

    @public_views_bp.route("/dev", methods=['GET'])
    def dev():
        return render_template_with_class("dev")

    return public_views_bp


def create_private_views_blueprint():
    private_views_bp = Blueprint("private", __name__, url_prefix="/")

    @private_views_bp.before_request
    @login_required
    def require_login():
        pass  # login_required will intercept and redirect unauthenticated user

    @private_views_bp.route("/dashboard", methods=['GET'])
    def dashboard():
        return render_template_with_class("dashboard")

    @private_views_bp.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('public.index'))

    @private_views_bp.route("/profile", methods=['GET'])
    def profile():
        return render_template_with_class("profile", has_js=False)

    @private_views_bp.route("/modals/message", methods=['GET'])
    def display_message_modal():
        return render_template(
            "modals/message.modal.html",
            message=request.args.get('message', '')
        )

    @private_views_bp.route("/modals/confirmation", methods=['GET'])
    def display_confirmation_modal():
        return render_template(
            "modals/confirmation.modal.html",
            message=request.args.get('message', '')
        )

    @private_views_bp.route("/modals/error", methods=['GET'])
    def display_error_modal():
        return render_template(
            "modals/error.modal.html",
            message=request.args.get('message', ''),
            stacktrace=request.args.get('stacktrace', ''),
            debug=current_app.debug
        )

    # TODO served as temporary to load the pages without adding new routes
    # To be replaced with actual routes
    # and clear up after the pages are fully implemented
    @private_views_bp.route("/pages/<name>", methods=['GET'])
    @private_views_bp.route("/components/<name>", methods=['GET'])
    @private_views_bp.route("/modals/<name>", methods=['GET'])
    def render_section(name):
        section = request.path.strip("/").split("/", 1)[0]
        return render_fragment(
            section,
            name
        )

    private_views_bp.register_blueprint(requests_views_bp)
    return private_views_bp


__all__ = ["create_public_views_blueprint", "create_private_views_blueprint"]
