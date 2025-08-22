from custom_logging.handler.impl import handler
from custom_logging.log_factory.impl import Log_Factory

logger = Log_Factory(handler=handler)
