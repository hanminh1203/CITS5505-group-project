from flask import Blueprint, jsonify
from models import Request, User
from schemas import RequestSchema

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

# TODO Define another schema for list API
requests_schema = RequestSchema(many=True)
request_schema = RequestSchema()

@requests_bp.route('/', methods=['GET'])
def get_requests():
    requests = Request.query.all()
    return requests_schema.jsonify(requests)

@requests_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.get_or_404(request_id)
    return request_schema.jsonify(request)