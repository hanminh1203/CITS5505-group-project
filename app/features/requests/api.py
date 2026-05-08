from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import (
    InvalidActionException,
    NotAuthorizedActionException,
    NotFoundException,
    ValidationException,
)
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


@requests_api_bp.route("/<int:request_id>/complete", methods=["POST"])
def complete_request(request_id):
    entity = db.get_or_404(Request, request_id)
    if entity.owner_id != current_user.id:
        raise NotAuthorizedActionException()
    if not entity.status.can_complete():
        raise InvalidActionException(
            "Request cannot be marked as completed in its current status."
        )
    entity.status = RequestStatus.COMPLETED
    db.session.commit()
    return jsonify(id=entity.id), 200


@requests_api_bp.route("/<int:request_id>/cancel", methods=["POST"])
def cancel_request(request_id):
    entity = db.get_or_404(Request, request_id)
    if entity.owner_id != current_user.id:
        raise NotAuthorizedActionException()
    if not entity.status.can_cancel():
        raise InvalidActionException(
            "Request cannot be cancelled in its current status."
        )
    entity.status = RequestStatus.CANCELLED
    db.session.commit()
    return jsonify(id=entity.id), 200


@requests_api_bp.route(
    "/<int:request_id>/offers/<int:offer_id>",
    methods=["DELETE"],
)
def cancel_offer(request_id, offer_id):
    entity = db.get_or_404(Request, request_id)

    offer = next(
        (offer for offer in entity.offers if offer.id == offer_id),
        None,
    )
    if not offer:
        raise NotFoundException("Offer not found.")
    if offer.offer_skill.user_id != current_user.id:
        raise NotAuthorizedActionException(
            "You are not authorized to cancel this offer."
        )

    db.session.delete(offer)
    db.session.commit()
    return jsonify(id=offer.id), 200
