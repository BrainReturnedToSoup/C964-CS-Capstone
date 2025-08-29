from http import HTTPStatus

def test_controller(test_client):
    valid_data={
        "SquareFeet": 2187,
        "Bathrooms": 1,
        "Bedrooms": 2,
        "Neighborhood": "Urban"
    }
    
    response=test_client.post("/predict", json=valid_data, base_url="https://localhost")
    
    assert response.status_code == HTTPStatus.OK
    
    assert "price_predictions" in response.json
    assert "gaussian_noisy_square_feet" in response.json