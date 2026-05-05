from math import ceil

from flask import Blueprint, current_app, render_template, request
from flask_login import current_user

from app.models import Request
from app.models.enums import RequestStatus, SkillLevel, SessionFormat
from app.extensions import db
from app.forms.request import RequestForm
from app.config import Config

requests_views_bp = Blueprint(
    "requests_views",
    __name__,
    url_prefix="/requests",
)


@requests_views_bp.route("/", methods=["GET"])
def get_requests():
    query = request.args.get("query", "", type=str).strip()
    status = request.args.get("status", "", type=str).strip()
    level = request.args.get("level", "", type=str).strip()
    format_value = request.args.get("format", "", type=str).strip()
    page = request.args.get("page", 1, type=int)

    page_size = Config.REQUESTS_PAGE_SIZE

    base_query = Request.query.filter(
        Request.status.in_([RequestStatus.OPEN, RequestStatus.PENDING])
    )

    # User should not search his/her own requests
    base_query = base_query.filter(Request.owner_id != current_user.id)

    # Search by title only
    if query:
        base_query = base_query.filter(Request.title.contains(query))

    # Optional filters
    if status:
        base_query = base_query.filter(Request.status == RequestStatus(status))

    if level:
        base_query = base_query.filter(Request.owner_skill.has(level=level))

    if format_value:
        base_query = base_query.filter(Request.format == format_value)

    total_items = base_query.count()
    total_pages = max(1, ceil(total_items / page_size))

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    requests_list = (
        base_query.order_by(Request.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    search = {
        "query": query,
        "status": status,
        "level": level,
        "format": format_value,
    }

    pagination = {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
    }

    return render_template(
        "pages/requests.page.html",
        requests=requests_list,
        search=search,
        pagination=pagination,
        css_file="/css/pages/requests.page.css",
        main_class="requests",
        SkillLevel=SkillLevel,
        SessionFormat=SessionFormat,
    )


@requests_views_bp.route("/<int:request_id>", methods=["GET"])
def get_request(request_id):
    request_item = Request.query.get_or_404(request_id)
    return render_template(
        "pages/request.page.html",
        request=request_item,
        css_file="/css/pages/request.page.css",
        main_class="request",
        js_file="/js/pages/request.page.js",
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
