from enum import Enum

class LogKeys(Enum):
    LOG_ORIGIN="log-origin"
    ROUTE="route"
    METHOD="method"
    REQUEST="request"
    EXCEPTION_RAISED="exception-raised"
    
class LogVals(Enum):
    [LogKeys.LOG_ORIGIN]="controllers.root.GET"
    [LogKeys.ROUTE]="/"
    [LogKeys.METHOD]="GET"
    