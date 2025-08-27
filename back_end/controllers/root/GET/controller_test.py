from http import HTTPStatus

def test_controller(test_client):
    response=test_client.get("/", base_url="https://localhost")
    
    assert response.status_code == HTTPStatus.OK
    