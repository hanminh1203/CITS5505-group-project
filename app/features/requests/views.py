from flask import Blueprint, render_template
from sqlalchemy.orm import selectinload

from app.forms import RequestForm
from app.models import Offer, Request, Skill, UserSkill

requests_views_bp = Blueprint("requests_views", __name__, url_prefix="/requests")


@requests_views_bp.route("/", methods=["GET"])
def get_requests():
    return render_template(
        "pages/requests.page.html",
        css_file="/css/pages/requests.page.css",
        main_class="requests",
    )


@requests_views_bp.route("/<int:request_id>", methods=["GET"])
def get_request(request_id):
    selected_request = Request.query.options(
        selectinload(Request.owner),
        selectinload(Request.offers).selectinload(Offer.offerer).selectinload(UserSkill.user),
        selectinload(Request.offers).selectinload(Offer.offerer).selectinload(UserSkill.skill).selectinload(Skill.category),
    ).get_or_404(request_id)
    return render_template(
        "pages/request.page.html",
        request=selected_request,
        css_file="/css/pages/request.page.css",
        js_file="js/pages/request.page.js",
        main_class="request",
    )


@requests_views_bp.route("/<int:request_id>/edit", methods=["GET"])
def get_request_edit_modal(request_id):
    selected_request = Request.query.get_or_404(request_id)
    form = RequestForm(obj=selected_request)
    return render_template("modals/request.modal.html", form=form)