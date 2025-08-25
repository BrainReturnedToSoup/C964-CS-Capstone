import pytest 

@pytest.mark.order(-1)
def test_controller(test_client):
    response=test_client.post("/predict", json={})