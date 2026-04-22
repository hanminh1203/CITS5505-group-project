
from flask import Blueprint, render_template
from sqlalchemy.orm import selectinload

from forms.request import RequestForm
from models import Offer, UserSkill, Request, Skill
from schemas import RequestSchema

request_schema = RequestSchema()
requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

@requests_bp.route('/', methods=['GET'])
def get_requests():
    return render_template(f"pages/requests.page.html", css_file='/css/pages/requests.page.css', main_class='requests')

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
    return render_template(f"pages/request.page.html", request = request, css_file='/css/pages/request.page.css', js_file='js/pages/request.page.js', main_class='request')

@requests_bp.route('/<int:request_id>/edit', methods=['GET'])
def get_request_edit_modal(request_id):
    request = Request.query.get_or_404(request_id)
    form = RequestForm(obj = request)
    return render_template(f"modals/request.modal.html", form = form);