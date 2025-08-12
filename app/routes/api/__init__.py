from flask import Blueprint
from ...extensions import csrf

api_bp = Blueprint("api", __name__, url_prefix="/api")
csrf.exempt(api_bp)   # <<— supaya POST dari Postman tidak ditolak CSRF

from . import predict  # noqa
