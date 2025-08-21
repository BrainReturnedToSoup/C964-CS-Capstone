from flask import request 
from predict.blueprint import bp
from .impl import Controller
from logging.logger_instance import logger

ctlr = Controller(logger=logger) 

@bp.route(methods=["POST"])
def controller():
    return ctlr.handle(request)