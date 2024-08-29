import pytest
from unittest.mock import patch, Mock
from .fixtures.common import mock_api_consumer_using_base_helpers

"""
These tests are for the common methods of the ApiConsumer Base Class.
These are tested using a mock class that uses the helper methods from the Base Class.
The responses are mocked using the unittest.mock module.
"""


@pytest.fixture
def api_headers_basic():
    return {"Content-Type": "application/json", "Accept": "application/json"}


@patch("requests.request")
def test_common_get(
    mock_request, mock_api_consumer_using_base_helpers, api_headers_basic
):
    # GIVEN - a mock API consumer
    api_consumer = mock_api_consumer_using_base_helpers("http://example.com")
    # GIVEN - a mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # WHEN - a GET request is made
    response = api_consumer.common_get("test/path")

    # THEN - the response should be as expected
    assert response == {"key": "value"}

    # THEN - the request should be made with the correct parameters
    mock_request.assert_called_once_with(
        "GET", "http://example.com/test/path", headers=api_headers_basic
    )


@patch("requests.request")
def test_common_post(
    mock_request, mock_api_consumer_using_base_helpers, api_headers_basic
):
    # GIVEN - a mock API consumer
    api_consumer = mock_api_consumer_using_base_helpers("http://example.com")

    # GIVEN - a mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # WHEN - a POST request is made
    response = api_consumer.common_post("test/path", data={"data": "value"})

    # THEN - the response should be as expected
    assert response == {"key": "value"}

    # THEN - the request should be made with the correct parameters
    mock_request.assert_called_once_with(
        "POST",
        "http://example.com/test/path",
        data={"data": "value"},
        headers=api_headers_basic,
    )


@patch("requests.request")
def test_common_put(
    mock_request, mock_api_consumer_using_base_helpers, api_headers_basic
):
    # GIVEN - a mock API consumer
    api_consumer = mock_api_consumer_using_base_helpers("http://example.com")

    # GIVEN - a mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # WHEN - a PUT request is made
    response = api_consumer.common_put("test/path", json={"key": "value"})

    # THEN - the response should be as expected
    assert response == {"key": "value"}

    # THEN - the request should be made with the correct parameters
    mock_request.assert_called_once_with(
        "PUT",
        "http://example.com/test/path",
        json={"key": "value"},
        headers=api_headers_basic,
    )


@patch("requests.request")
def test_common_patch(
    mock_request, mock_api_consumer_using_base_helpers, api_headers_basic
):
    # GIVEN - a mock API consumer
    api_consumer = mock_api_consumer_using_base_helpers("http://example.com")

    # GIVEN - a mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # WHEN - a PATCH request is made
    response = api_consumer.common_patch("test/path", data={"data": "value"})

    # THEN - the response should be as expected
    assert response == {"key": "value"}

    # THEN - the request should be made with the correct parameters
    mock_request.assert_called_once_with(
        "PATCH",
        "http://example.com/test/path",
        data={"data": "value"},
        headers=api_headers_basic,
    )


@patch("requests.request")
def test_common_delete(
    mock_request, mock_api_consumer_using_base_helpers, api_headers_basic
):
    # GIVEN - a mock API consumer
    api_consumer = mock_api_consumer_using_base_helpers("http://example.com")

    # GIVEN - a mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # WHEN - a DELETE request is made
    response = api_consumer.common_delete("test/path")

    # THEN - the response should be as expected
    assert response == {"key": "value"}

    # THEN - the request should be made with the correct parameters
    mock_request.assert_called_once_with(
        "DELETE", "http://example.com/test/path", headers=api_headers_basic
    )
