from flask import request 
from root.blueprint import bp
from .impl import Controller
from custom_logging.logger_instance import logger

ctlr = Controller(logger=logger) 

@bp.route(rules="/", methods=["GET"])
def controller():
    return ctlr.handle(request)