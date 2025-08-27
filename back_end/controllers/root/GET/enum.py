from enum import Enum

class LogKeys(Enum):
    LOG_ORIGIN="log-origin"
    ROUTE="route"
    METHOD="method"
    REQUEST="request"
    EXCEPTION_RAISED="exception-raised"
    
LogVals={
    LogKeys.LOG_ORIGIN.value: "controllers.root.GET",
    LogKeys.ROUTE.value: "/",
    LogKeys.METHOD.value: "GET"
}