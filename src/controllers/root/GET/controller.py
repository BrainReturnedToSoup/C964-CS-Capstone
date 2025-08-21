from flask import request 
from root.blueprint import bp
from .impl import Controller

ctlr = Controller() 

@bp.route(methods=["GET"])
def controller():
    return ctlr.handle(request)

__all__ = ["Controller"]