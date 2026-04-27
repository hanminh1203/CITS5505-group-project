from flask import Blueprint, request

from app.extensions import db
from app.forms import RequestForm
from app.models import Request, SessionFormat
from app.schemas import RequestSchema

requests_api_bp = Blueprint("requests", __name__, url_prefix="/requests")

requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()


@requests_api_bp.route("/", methods=["POST"])
def update_request():
    dto = RequestForm(obj=request.form)
    entity = db.get_or_404(Request, dto.id.data)
    entity.title = dto.title.data
    entity.description = dto.description.data
    entity.format = SessionFormat(dto.format.data)
    entity.availability = dto.availability.data
    entity.duration = dto.duration.data
    db.session.commit()
    return "", 200
