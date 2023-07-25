from flask import Blueprint

main = Blueprint("main", __name__, url_prefix="/web")

from web.app.routers.main import urls
