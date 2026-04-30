from flask import Blueprint, render_template, request

from app.models import Request
from app.models.enums import RequestStatus

requests_views_bp = Blueprint(
    "requests_views",
    __name__,
    url_prefix="/requests",
)

PAGE_SIZE = 6


@requests_views_bp.route("/", methods=["GET"])
def get_requests():
    query = request.args.get("query", "").strip()
    status = request.args.get("status", "").strip()
    level = request.args.get("level", "").strip()
    format_value = request.args.get("format", "").strip()
    offset = request.args.get("offset", default=0, type=int)

    base_query = Request.query.filter(
        Request.status.in_([RequestStatus.OPEN, RequestStatus.PENDING])
    )

    # title search only, as required
    if query:
        base_query = base_query.filter(Request.title.ilike(f"%{query}%"))

    # optional filters for chip UI
    if status:
        base_query = base_query.filter(Request.status == RequestStatus(status))

    if level:
        base_query = base_query.filter(Request.owner_skill.has(level=level))

    if format_value:
        base_query = base_query.filter(Request.format == format_value)

    total = base_query.count()

    requests_list = (
        base_query.order_by(Request.created_at.desc())
        .offset(offset)
        .limit(PAGE_SIZE)
        .all()
    )

    has_prev = offset > 0
    has_next = offset + PAGE_SIZE < total
    prev_offset = max(offset - PAGE_SIZE, 0)
    next_offset = offset + PAGE_SIZE

    return render_template(
        "pages/requests.page.html",
        requests=requests_list,
        query=query,
        selected_status=status,
        selected_level=level,
        selected_format=format_value,
        offset=offset,
        prev_offset=prev_offset,
        next_offset=next_offset,
        has_prev=has_prev,
        has_next=has_next,
        total=total,
        css_file="/css/pages/requests.page.css",
        main_class="requests",
    )
