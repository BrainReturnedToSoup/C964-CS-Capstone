from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock
from back_end.custom_logging.instance import logger
from .impl import Controller

path=Path(__file__).resolve().parent.parent.parent

def test_handle():
    controller=Controller(logger=logger, template=path / "templates" / "index_test.html")
    
    valid_req=Mock()
    valid_req.is_secure=True
    
    response_valid=controller.handle(req=valid_req)
    
    assert isinstance(response_valid, Path)
    
    invalid_req=Mock()
    invalid_req.is_secure=False
    
    response_invalid=controller.handle(req=invalid_req)
    
    assert response_invalid.status_code == HTTPStatus.FORBIDDEN
    