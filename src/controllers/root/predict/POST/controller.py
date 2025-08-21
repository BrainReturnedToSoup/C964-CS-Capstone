from flask import request 
from predict.blueprint import bp
from .impl import Controller

ctlr = Controller() 

@bp.route(methods=["POST"])
def controller():
    return ctlr.handle(request)

__all__ = ["Controller"]