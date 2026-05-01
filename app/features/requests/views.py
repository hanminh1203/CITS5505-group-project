from math import ceil

from flask import Blueprint, current_app, render_template, request
from flask_login import current_user

from app.models import Request
from app.models.enums import RequestStatus

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

    page_size = current_app.config.get("REQUESTS_PAGE_SIZE", 6)

    base_query = Request.query.filter(
        Request.status.in_([RequestStatus.OPEN, RequestStatus.PENDING])
    )

    # User should not search his/her own requests
    if current_user.is_authenticated:
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
    )


@requests_views_bp.route("/<int:request_id>", methods=["GET"])
def get_request(request_id):
    request_item = Request.query.get_or_404(request_id)
    return render_template(
        "pages/request.page.html",
        request=request_item,
    )
