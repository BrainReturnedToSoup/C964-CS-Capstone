from flask import request, Response
from predict.blueprint import bp
from .impl import Controller
from custom_logging.instance import logger
from services.predicter.instance import predicter
from .interface import RequestBody

ctlr=Controller(logger=logger, predicter=predicter, response=Response, body_schema=RequestBody()) 

@bp.route(rule="/", methods=["POST"])
def controller():
    return ctlr.handle(request)