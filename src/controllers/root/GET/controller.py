from http import HTTPMethod
from flask import request 
from root.blueprint import bp
from .impl import Controller
from custom_logging.instance import logger

ctlr = Controller(logger=logger) 

@bp.route(rules="/", methods=[HTTPMethod.GET])
def controller():
    return ctlr.handle(request)