from custom_logging.handler.impl import handler
from custom_logging.log_factory.impl import LogFactory

logger = LogFactory(handler=handler)
