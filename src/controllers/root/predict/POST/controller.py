from flask import request, Response
from predict.blueprint import bp
from .impl import Controller
from logging.logger_instance import logger
from services.predict.instance import predicter
from .interface import RequestBodySchema

ctlr=Controller(logger=logger, predicter=predicter, response=Response, body_schema=RequestBodySchema()) 

@bp.route(methods=["POST"])
def controller():
    return ctlr.handle(request)