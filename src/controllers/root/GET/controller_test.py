from .controller import controller

def test_controller(test_client):
    response=test_client.get("/")
    assert "text/html" in response.content_type