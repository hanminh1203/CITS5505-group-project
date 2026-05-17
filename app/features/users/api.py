from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import ValidationException
from app.extensions import db
from app.forms import ProfileForm
from app.models import User

users_api_bp = Blueprint("users", __name__, url_prefix="/users")

# it is a put request to update the user profile
@users_api_bp.route("/me", methods=["PUT"])
def update_profile():
    # it will use ProfileForm to validate the request form
    dto = ProfileForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    # it will update the user profile by user id, if not found it will return a 404 error
    user = db.get_or_404(User, current_user.id)
    user.name = dto.name.data
    user.bio = dto.bio.data
    user.address = dto.address.data
    
    # commit the changes to the database
    db.session.commit()
    # return the user id and a 200 success status code
    return jsonify(id=user.id), 200
