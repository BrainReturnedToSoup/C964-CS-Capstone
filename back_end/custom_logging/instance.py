from .handler.impl import handler
from .log_factory.impl import LogFactory

logger = LogFactory(handler=handler)
