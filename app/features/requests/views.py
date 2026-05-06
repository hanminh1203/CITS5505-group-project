from flask import Blueprint, render_template, request
from flask_login import current_user

from app.extensions import db
from app.forms import RequestForm
from app.forms.offer import OfferForm
from app.models import Request

requests_views_bp = Blueprint(
    "requests_views",
    __name__,
    url_prefix="/requests",
)


@requests_views_bp.route("/", methods=["GET"])
def get_requests():
    return render_template(
        "pages/requests.page.html",
        css_file="/css/pages/requests.page.css",
        main_class="requests",
    )


@requests_views_bp.route("/<int:request_id>", methods=["GET"])
def get_request(request_id):
    selected_request = db.get_or_404(Request, request_id)
    offering = any(
        offer.offer_skill.user_id == current_user.id
        for offer in selected_request.offers
    )
    return render_template(
        "pages/request.page.html",
        request=selected_request,
        offering=offering,
        css_file="/css/pages/request.page.css",
        js_file="js/pages/request.page.js",
        main_class="request",
    )


@requests_views_bp.route("/modal", methods=["GET"])
def get_request_edit_modal():
    request_id = request.args.get('request_id')
    selected_request = (
        db.get_or_404(Request, request_id) if request_id else None
    )
    form = RequestForm(obj=selected_request)
    return render_template(
        "modals/request.modal.html",
        form=form,
        is_new=not request_id,
    )


@requests_views_bp.route("/<int:request_id>/offer", methods=["GET"])
def get_offer_modal(request_id):
    selected_request = db.get_or_404(Request, request_id)
    form = OfferForm()
    return render_template(
        "modals/offer.modal.html",
        form=form,
        request=selected_request,
    )
