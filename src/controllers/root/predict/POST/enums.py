from enum import Enum
class LogKeys(Enum):
    LOG_ORIGIN="log-origin"
    ROUTE="route"
    METHOD="method"
    REQUEST="request"
    EXCEPTION_RAISED="exception-raised"
    REQUEST_BODY="request-body"
    
LogVals={
    LogKeys.LOG_ORIGIN.value: "controllers.root.predict.POST",
    LogKeys.ROUTE.value: "/predict",
    LogKeys.METHOD.value: "POST"
}