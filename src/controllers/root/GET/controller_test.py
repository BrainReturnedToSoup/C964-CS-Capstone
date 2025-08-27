def test_controller(test_client):
    response=test_client.get("/", base_url="https://localhost")
    
    print(f"test_controller_GET={response}")
    