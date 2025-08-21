from flask import Blueprint
from .predict.blueprint import bp as child_bp

# create base bp
bp = Blueprint("root", __name__, url_prefix="/")

# register immediate children routes
bp.register_blueprint(child_bp)