from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, logout_user, current_user

from app.features.requests.views import requests_views_bp
from app.features.skills.page import skills_views_bp
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.extensions import db
from app.models.user import User


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


# --- Public Routes ---

@public_views_bp.route("/", methods=['GET'])
@public_views_bp.route("/index.html", methods=['GET'])
def index():
    return render_template_with_class("home")


@public_views_bp.route("/login", methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('private.dashboard'))
    return render_template_with_class('login', form=LoginForm())


    @public_views_bp.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("private.dashboard"))

        form = RegisterForm()

        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            name = form.name.data.strip()

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                form.email.errors.append("This email is already registered.")
                return render_template_with_class(
                    "register",
                    has_js=False,
                    form=form,
                )

            user = User(
                name=name,
                email=email,
                )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash("Register successful. Please log in.", "success")
            return redirect(url_for("public.login"))

        return render_template_with_class(
            "register",
            has_js=False,
            form=form,
        )


@public_views_bp.route("/dev", methods=['GET'])
def dev():
    return render_template_with_class("dev")


def create_public_views_blueprint():
    return public_views_bp


# --- Private Routes ---

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
    skills = (
        Skill.query.filter_by(user_id=current_user.id)
        .order_by(db.func.lower(Skill.name).asc())
        .all()
    )
    return render_template_with_class(
        "profile", skills=skills, form=SkillForm()
    )


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


def create_private_views_blueprint():
    private_views_bp.register_blueprint(requests_views_bp)
    private_views_bp.register_blueprint(skills_views_bp)
    return private_views_bp


__all__ = ["create_public_views_blueprint", "create_private_views_blueprint"]
