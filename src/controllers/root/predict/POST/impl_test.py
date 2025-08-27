import json
from http import HTTPStatus
from unittest.mock import Mock
from .impl import Controller
from services.predicter.monte_carlo.instance import monte_carlo_predicter
from custom_logging.instance import logger

def test_handle():
    controller=Controller(logger=logger, monte_carlo_predicter=monte_carlo_predicter)  
    
    valid_body=json.dumps({
        "SquareFeet": 1876,
        "Bathrooms": 2,
        "Bedrooms": 2,
        "Neighborhood": "Urban"
    })
    
    valid_req=Mock()
    valid_req.is_secure=True
    valid_req.is_json=True
    valid_req.get_json=Mock(return_value=valid_body)
    
    response=controller.handle(valid_req)
    
    assert response.status_code == int(HTTPStatus.OK)
    assert response.content_type == "application/json"
    assert "price_predictions" in json.dumps(response.get_json())
    assert "noisy_inputs" in json.dumps(response.get_json())
    
    invalid_req_1=Mock()
    invalid_req_1.is_secure=False # invalid
    invalid_req_1.is_json=True
    invalid_req_1.get_json=Mock(return_value=valid_body)
    
    response=controller.handle(invalid_req_1)
    
    assert response.status_code == int(HTTPStatus.FORBIDDEN)
    
    invalid_req_2=Mock()
    invalid_req_2.is_secure=True
    invalid_req_2.is_json=False # invalid
    
    response=controller.handle(invalid_req_2)
    
    assert response.status_code == int(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    
    invalid_body_1=json.dumps({
        "SquareFeet": 0, # invalid
        "Bathrooms": 2,
        "Bedrooms": 2,
        "Neighborhood": "Urban"
    })
    
    invalid_body_2=json.dumps({
        "SquareFeet": 1876, 
        "Bathrooms": 4, # invalid
        "Bedrooms": 2,
        "Neighborhood": "Urban"
    })
    
    invalid_body_3=json.dumps({
        "SquareFeet": 1876,
        "Bathrooms": 2,
        "Bedrooms": 0, # invalid
        "Neighborhood": "Urban"
    })
    
    invalid_body_4=json.dumps({
        "SquareFeet": 1876,
        "Bathrooms": 2,
        "Bedrooms": 2,
        "Neighborhood": "invalid" # invalid
    })
    
    invalid_req_3=Mock()
    invalid_req_3.is_secure=True
    invalid_req_3.is_json=True
    invalid_req_3.get_json=Mock(return_value=invalid_body_1) # invalid
    
    response=controller.handle(invalid_req_3)
    
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    
    invalid_req_4=Mock()
    invalid_req_4.is_secure=True
    invalid_req_4.is_json=True
    invalid_req_4.get_json=Mock(return_value=invalid_body_2) # invalid
    
    response=controller.handle(invalid_req_4)
    
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    
    invalid_req_5=Mock()
    invalid_req_5.is_secure=True
    invalid_req_5.is_json=True
    invalid_req_5.get_json=Mock(return_value=invalid_body_3) # invalid
    
    response=controller.handle(invalid_req_5)
    
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    
    invalid_req_6=Mock()
    invalid_req_6.is_secure=True
    invalid_req_6.is_json=True
    invalid_req_6.get_json=Mock(return_value=invalid_body_4) # invalid
    
    response=controller.handle(invalid_req_6)
    
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)