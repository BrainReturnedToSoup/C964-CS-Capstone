from http import HTTPMethod
from flask import request 
from pathlib import Path
from controllers.root.blueprint import bp
from .impl import Controller
from custom_logging.instance import logger

template_path=Path(__name__).resolve().parent.parent.parent / "templates" / "index_test.html"

ctlr = Controller(logger=logger, template_path=template_path) 

@bp.route(rule="/", methods=[HTTPMethod.GET])
def controller():
    return ctlr.handle(request)