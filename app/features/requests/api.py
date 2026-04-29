from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import NotAuthorizedActionException, ValidationException
from app.extensions import db
from app.forms import RequestForm
from app.forms.offer import OfferForm
from app.models import Request, SessionFormat, Offer
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
        if entity.owner_id != current_user.id:
            raise NotAuthorizedActionException()
    else:
        entity = Request()
        entity.owner_id = current_user.id
        entity.status = RequestStatus.OPEN
        db.session.add(entity)

    entity.title = dto.title.data
    entity.description = dto.description.data
    entity.owner_skill_id = dto.owner_skill.data.id
    entity.skill_to_learn = dto.skill_to_learn.data
    entity.format = SessionFormat(dto.format.data) if dto.format.data else None
    entity.availability = dto.availability.data
    entity.duration = dto.duration.data
    db.session.commit()
    return jsonify(id=entity.id), 200


@requests_api_bp.route("/<int:request_id>/offer", methods=["POST"])
def make_offer(request_id):
    selected_request = db.get_or_404(Request, request_id)
    if selected_request.owner_id == current_user.id:
        raise NotAuthorizedActionException(
            "You cannot make an offer on your own request."
        )

    dto = OfferForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    entity = Offer()
    entity.request_id = request_id
    entity.offer_skill_id = dto.skill.data.id
    entity.message = dto.message.data
    db.session.add(entity)

    if selected_request.status == RequestStatus.OPEN:
        selected_request.status = RequestStatus.PENDING
    db.session.commit()
    return jsonify(id=entity.id), 200