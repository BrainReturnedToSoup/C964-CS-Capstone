from custom_logging.handler.impl import handler
from .impl import LogFactory
from custom_logging.log.impl import Log

def test_log_factory():
    log_factory=LogFactory(handler)
    
    # ensure the handler supplied is the handler saved
    assert log_factory.handler == handler
    
    log = log_factory.create_log()
    
    # ensure the log created has all the right state, handler injected by the log factory
    assert isinstance(log, Log)
    assert log.handler == handler
    assert log.data == {}
    assert log.commited == False
    
    # ensure the handler even after injection stays the same in the log factor
    assert log_factory.handler == handler