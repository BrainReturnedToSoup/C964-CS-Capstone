from custom_logging.handler.impl import handler
from custom_logging.log_factory.impl import Log_Factory

# testing to ensure the log factory can be created, and reused throughout the 
# application. This test assumes that the individual parts were tested for correctness
# (things like the state machine of the log factory, the log, and handler itself)
# you can add more tests based on the handler you create, but this will require making a 'slice' of tests all the way up, since these 
# execute in a specific order to reuse previous tests in their coverage. 

mock_key_atr_set_1 = {
    "1": "mock",
    "2": ["mock"],
    "3": {"mock": "mock"},
    "4": ("mock")
}

mock_key_atr_set_2 = {
    "5": "mock",
    "6": ["mock"],
    "7": {"mock": "mock"},
    "8": ("mock")
}

def test_logger(capsys):
    # check and create the logger factory
    assert capsys.readouterr().out == ""
    
    logger = Log_Factory(handler=handler)
    
    # create a new log and assert that on commit it reads out to stdout
    log_1 = logger.create_log()
    
    assert capsys.readouterr().out == ""
    
    for key in mock_key_atr_set_1:
        log_1.add_attribute(key, mock_key_atr_set_1[key])
        
    log_1.commit()
    
    assert capsys.readouterr().out.strip("\n") == str(mock_key_atr_set_1)
    
    
    # create a second new log from the same logger and assert that on commit it reads out to stdout
    log_2 = logger.create_log()
    
    assert capsys.readouterr().out == ""
    
    for key in mock_key_atr_set_2:
        log_2.add_attribute(key, mock_key_atr_set_2[key])
        
    log_2.commit()
    
    assert capsys.readouterr().out.strip("\n") == str(mock_key_atr_set_2)
    
    