from flask import Flask
import pytest

@pytest.fixture
def test_client():
    app=Flask(__name__)
    app.config.update({"TESTING": True})
    
    return app.test_client()