from flask import request, render_template, Blueprint
from .impl import Controller
from back_end.custom_logging.instance import logger

# represents '/' GET, the endpoint that serves the frontend for this application.

bp=Blueprint("root-GET", import_name=__name__)

ctlr=Controller(logger=logger, template="index.html") 

@bp.route(rule="/", methods=["GET"])
def controller():
    return render_template(ctlr.handle(request))