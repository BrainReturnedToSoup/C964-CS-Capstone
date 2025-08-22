import pytest
from .impl import Log
from ..handler.impl import handler

# testing for proper log state machine. Not making assertions on invalid data types though

mock_key_1="mock_key_1"
mock_val_1="mock_val"

mock_key_2="mock_key_2"
mock_val_2=["mock_val_2"]

mock_key_3="mock_key_3"
mock_val_3={"mock": "val_3"}

mock_key_4="mock_key_4"
mock_val_4=("mock_val_4")

def test_log():
    log = Log(handler=handler)
    
    assert log.handler == handler
    assert log.data == {}
    assert log.commited == False
        
    log.add_attribute(mock_key_1, mock_val_1)
    
    assert mock_key_1 in log.data
    assert mock_val_1 == log.data[mock_key_1]
    
    log.add_attribute(mock_key_2, mock_val_2)
    
    assert mock_key_1 in log.data
    assert mock_val_1 == log.data[mock_key_1]
    assert mock_key_2 in log.data
    assert mock_val_2 == log.data[mock_key_2]
    
    log.add_attribute(mock_key_3, mock_val_3)
    
    assert mock_key_1 in log.data
    assert mock_val_1 == log.data[mock_key_1]
    assert mock_key_2 in log.data
    assert mock_val_2 == log.data[mock_key_2]
    assert mock_key_3 in log.data
    assert mock_val_3 == log.data[mock_key_3]
    
    log.add_attribute(mock_key_4, mock_val_4)
    
    assert mock_key_1 in log.data
    assert mock_val_1 == log.data[mock_key_1]
    assert mock_key_2 in log.data
    assert mock_val_2 == log.data[mock_key_2]
    assert mock_key_3 in log.data
    assert mock_val_3 == log.data[mock_key_3]
    assert mock_key_4 in log.data
    assert mock_val_4 == log.data[mock_key_4]

    # should raise exception because the key-val pair was already added   
    with pytest.raises(Exception) as e:

        log.add_attribute(mock_key_1, mock_val_1)
        
    assert "key-already-exists" == str(e.value)
    
    # ensure the other members haven't changed
    assert log.commited == False
    assert log.handler == handler
    
    log.commit()
    
    # ensure the commited flag changes on the first commit to True
    assert log.commited == True 
    
    # should raise exception because the log was already commited
    with pytest.raises(Exception) as e:
        
        log.commit()
    
    assert "log-commited" == str(e.value)
    
    