from flask import Blueprint, request
from sqlalchemy.orm import selectinload

from forms.request import RequestForm
from models import Offer, Request, SessionFormat, Skill, UserSkill
from schemas import RequestSchema
from configs.database import db

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

# TODO Define another schema for list API
requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()

@requests_bp.route('/', methods=['GET'])
def get_requests():
    requests = Request.query.options(
        selectinload(Request.owner),
        selectinload(Request.offers)
        .selectinload(Offer.offerer)
        .selectinload(UserSkill.user),
        selectinload(Request.offers)
        .selectinload(Offer.offerer)
        .selectinload(UserSkill.skill)
        .selectinload(Skill.category),
    ).order_by(Request.id).all()
    return requests_schema.jsonify(requests)

@requests_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.options(
        selectinload(Request.owner),
        selectinload(Request.offers)
        .selectinload(Offer.offerer)
        .selectinload(UserSkill.user),
        selectinload(Request.offers)
        .selectinload(Offer.offerer)
        .selectinload(UserSkill.skill)
        .selectinload(Skill.category),
    ).get_or_404(request_id)
    return request_schema.jsonify(request)

@requests_bp.route('/', methods=['POST'])
def update_request():
    dto = RequestForm(obj = request.form)
    entity = Request.query.get_or_404(dto.id.data)
    entity.title = dto.title.data
    entity.description = dto.description.data
    entity.format = SessionFormat(dto.format.data)
    entity.availability = dto.availability.data
    entity.duration = dto.duration.data
    db.session.commit()
    return '', 200