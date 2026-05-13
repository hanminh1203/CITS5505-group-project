from flask import Blueprint, render_template
from flask_login import current_user

from app.forms.profile import ProfileForm

users_views_bp = Blueprint("users_views", __name__)


@users_views_bp.route("/modals/profile", methods=['GET'])
def display_profile_modal():
    form = ProfileForm(obj=current_user)
    return render_template(
        "modals/profile.modal.html", profile_form=form
    )
