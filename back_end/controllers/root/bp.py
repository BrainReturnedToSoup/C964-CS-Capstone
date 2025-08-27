from flask import Blueprint
from .GET.controller import bp as GET_bp
from .predict.bp import bp as predict_bp

bp=Blueprint(name="root", import_name=__name__, url_prefix="/")
bp.register_blueprint(blueprint=GET_bp)
bp.register_blueprint(blueprint=predict_bp)