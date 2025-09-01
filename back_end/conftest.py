from .app import create_app
import pytest

@pytest.fixture
def test_client():
    app = create_app()
    with app.test_client() as client:
        yield client