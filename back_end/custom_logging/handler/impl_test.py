import pytest
from .impl import handler

mock_log_1 = {"mock": "log"}
mock_log_2 = {"mock": ["log"]}
mock_log_3 = {"mock": {"log": "three"}}
mock_log_4 = {"mock": ("log", "four")}

# Testing the handler to ensure it prints to terminal, ensuring proper matching
@pytest.mark.order(1)
def test_handler(capsys):
    assert capsys.readouterr().out == ""
    
    handler(mock_log_1)
    assert capsys.readouterr().out.strip("\n") == str(mock_log_1)
    
    handler(mock_log_2)
    assert capsys.readouterr().out.strip("\n") == str(mock_log_2)
    
    handler(mock_log_3)
    assert capsys.readouterr().out.strip("\n") == str(mock_log_3)
    
    handler(mock_log_4)
    assert capsys.readouterr().out.strip("\n") == str(mock_log_4)
    
