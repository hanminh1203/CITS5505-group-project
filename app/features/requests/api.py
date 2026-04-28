from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import ValidationException
from app.extensions import db
from app.forms import RequestForm
from app.models import Request, SessionFormat
from app.models.enums import RequestStatus
from app.schemas import RequestSchema

requests_api_bp = Blueprint("requests", __name__, url_prefix="/requests")

requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()


@requests_api_bp.route("/", methods=["POST"])
def update_request():
    dto = RequestForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    entity = None
    if dto.id.data:
        entity = db.get_or_404(Request, dto.id.data)
    else:
        entity = Request()
        entity.owner_id = current_user.id
        entity.status = RequestStatus.OPEN
        db.session.add(entity)

    entity.title = dto.title.data
    entity.description = dto.description.data
    entity.owner_skill_id = dto.skill_to_offer.data
    entity.skill_to_learn = dto.skill_to_learn.data
    entity.format = SessionFormat(dto.format.data)
    entity.availability = dto.availability.data
    entity.duration = dto.duration.data
    db.session.commit()
    return jsonify(id=entity.id), 200
