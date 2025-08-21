from flask import request 
from predict.blueprint import bp
from .impl import Controller
from logging.logger_instance import logger
from services.predict.instance import predicter

ctlr = Controller(logger=logger, predicter=predicter) 

@bp.route(methods=["POST"])
def controller():
    return ctlr.handle(request)