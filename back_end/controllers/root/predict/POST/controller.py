from flask import request, Blueprint
from .impl import Controller
from back_end.custom_logging.instance import logger
from back_end.services.predictor.monte_carlo.instance import monte_carlo_predictor

# represents '/predict' POST, the endpoint for the actual predictions

bp=Blueprint("predict-POST", import_name=__name__)

ctlr=Controller(logger=logger, monte_carlo_predictor=monte_carlo_predictor, num_of_samples=1000) 

@bp.route(rule="/", methods=["POST"])
def controller():
    return ctlr.handle(request)