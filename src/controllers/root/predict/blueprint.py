from flask import Blueprint

bp = Blueprint(name="predict", import_name=__name__, url_prefix="/predict")

__all__ = ["bp"]