from flask import Blueprint
from .POST.controller import bp as POST_bp

bp=Blueprint(name="predict", import_name=__name__, url_prefix="/predict")
bp.register_blueprint(POST_bp)