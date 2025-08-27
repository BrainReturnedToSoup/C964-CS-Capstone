from flask import request, Response, Blueprint
from .impl import Controller
from custom_logging.instance import logger
from services.predictor.monte_carlo.instance import monte_carlo_predictor

bp=Blueprint("predict-POST", import_name=__name__)

ctlr=Controller(logger=logger, monte_carlo_predictor=monte_carlo_predictor, num_of_samples=1000) 

@bp.route(rule="/", methods=["POST"])
def controller():
    return ctlr.handle(request)