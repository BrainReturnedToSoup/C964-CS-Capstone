from enum import Enum

class LogKeys(Enum):
    log_origin="log-origin"
    route="route"
    method="method"
    request="request"
    exception_raised="exception-raised"
    
class LogVals(Enum):
    [LogKeys.log_origin]="controllers.root.predict.POST"
    [LogKeys.route]="/predict"
    [LogKeys.method]="POST"
    