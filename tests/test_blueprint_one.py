"""PyTest, Tests the hello API endpoint."""

from flask.testing import FlaskClient

from mycoolapp import create_app


def test_hello(client: FlaskClient) -> None:
    """Test the hello API endpoint. This one uses the fixture in conftest.py."""
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, World!"


def test_hello_with_config(get_test_config: dict) -> None:
    """Test the hello API endpoint with non-default config."""
    app = create_app(get_test_config("different_my_message"))
    client = app.test_client()
    response = client.get("/hello/")
    assert response.json["msg"] == "Hello, PyTest!"