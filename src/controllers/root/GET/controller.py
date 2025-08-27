from flask import request, render_template, Blueprint
from .impl import Controller
from custom_logging.instance import logger

bp=Blueprint("root-GET", import_name=__name__)

ctlr=Controller(logger=logger, template="index_test.html") 

@bp.route(rule="/", methods=["GET"])
def controller():
    return render_template(ctlr.handle(request))