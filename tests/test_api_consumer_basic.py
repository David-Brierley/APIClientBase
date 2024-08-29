import pytest
from pydantic import ValidationError
from tests.fixtures.common import mock_api_consumer_basic
from api_client_base.core.api_consumer import ApiConsumer

"""
These tests are for the basic functionality of the ApiConsumer Base Class.
A simple mock class is used to test the basic functionality of the Base Class.
"""


# Test cases
def test_valid_base_url(mock_api_consumer_basic):
    # Given - a mock API consumer
    consumer = mock_api_consumer_basic("https://example.com")

    # Then - the base URL should be set
    assert consumer.base_url == "https://example.com"


def test_invalid_base_url(mock_api_consumer_basic):
    # Given - a mock API consumer

    # When - an invalid base URL is provided

    # Then - a validation error should be raised
    with pytest.raises(ValidationError):
        mock_api_consumer_basic("httpppp://example.com")


def test_get_method(mock_api_consumer_basic):
    # Given - a mock API consumer
    consumer = mock_api_consumer_basic("https://example.com")

    # When - a GET request is made
    response = consumer.get("/test")

    # Then - the response should be as expected
    assert response == "GET request to https://example.com/test"


def test_post_method(mock_api_consumer_basic):
    # Given - a mock API consumer
    consumer = mock_api_consumer_basic("https://example.com")

    # When - a POST request is made
    response = consumer.post("/test")

    # Then - the response should be as expected
    assert response == "POST request to https://example.com/test"
