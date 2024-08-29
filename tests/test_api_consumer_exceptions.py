import pytest
from unittest.mock import patch, Mock
from requests.exceptions import (
    HTTPError as ReqHTTPError,
    ConnectionError as ReqConnectionError,
    Timeout as ReqTimeout,
    RequestException as ReqRequestException,
)
from api_client_base.core.exceptions import (
    HTTPError,
    ConnectionError,
    TimeoutError,
    RequestError,
    UnexcpectedError,
)
from api_client_base.core.api_consumer import ApiConsumer
from .fixtures.exceptions import mock_api_consumer_for_exceptions

"""
These tests test the correct exceptions are raised when the _make_request method is called
The make request method should handle the requests exceptions and raise the correct exceptions which we have defined in the core.exceptions module
"""


@patch("requests.request")
def test_make_request_http_error(mock_request, mock_api_consumer_for_exceptions):
    # GIVEN - A mocked response with an HTTP error
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = ReqHTTPError(
        "404 Client Error: Not Found for url: https://example.com/api/test"
    )
    mock_response.status_code = 404
    mock_request.return_value = mock_response

    # print(type(mock_response.raise_for_status.side_effect))

    # AND - A MockApiConsumer instance
    consumer = mock_api_consumer_for_exceptions(base_url="https://example.com")

    # THEN - An HTTPError should be raised when _make_request is called
    with pytest.raises(HTTPError) as excinfo:
        consumer.get("api/test")

    # AND - The correct message should be displayed
    assert (
        str(excinfo.value)
        == "Request Error: Request to URL failed with HTTP code 404: 404 Client Error: Not Found for url: https://example.com/api/test"
    )


@patch("requests.request")
def test_make_request_connection_error(mock_request, mock_api_consumer_for_exceptions):
    # GIVEN - A mocked response with a connection error
    mock_request.side_effect = ReqConnectionError(
        "Connection error occurred when trying to reach https://example.com/api/test"
    )

    # AND - A MockApiConsumer instance
    consumer = mock_api_consumer_for_exceptions(base_url="https://example.com")

    # THEN - A ConnectionError should be raised when _make_request is called
    with pytest.raises(ConnectionError) as excinfo:
        consumer.get("api/test")

    # AND - The correct message should be displayed
    assert (
        str(excinfo.value)
        == "Connection error: Connection error occurred when trying to reach https://example.com/api/test"
    )


@patch("requests.request")
def test_make_request_timeout_error(mock_request, mock_api_consumer_for_exceptions):
    # GIVEN - A mocked response with a timeout error
    mock_request.side_effect = ReqTimeout(
        "Request to https://example.com/api/test timed out"
    )

    # AND - A MockApiConsumer instance
    consumer = mock_api_consumer_for_exceptions(base_url="https://example.com")

    # THEN - A TimeoutError should be raised when _make_request is called
    with pytest.raises(TimeoutError) as excinfo:
        consumer.get("api/test")

    # AND - The correct message should be displayed
    assert (
        str(excinfo.value)
        == "Request timed out: Request to https://example.com/api/test timed out"
    )


@patch("requests.request")
def test_make_request_request_exception(mock_request, mock_api_consumer_for_exceptions):
    # GIVEN - A mocked response with a generic request exception
    mock_request.side_effect = ReqRequestException("Generic request error")

    # AND - A MockApiConsumer instance
    consumer = mock_api_consumer_for_exceptions(base_url="https://example.com")

    # THEN - A RequestError should be raised when _make_request is called
    with pytest.raises(RequestError) as excinfo:
        consumer.get("api/test")

    # AND - The correct message should be displayed
    assert (
        str(excinfo.value)
        == "Request error: Request error occurred: Generic request error"
    )


@patch("requests.request")
def test_make_request_request_error(mock_request, mock_api_consumer_for_exceptions):
    # GIVEN - A mocked response with a generic request error
    mock_request.side_effect = Exception("Generic request error")

    # AND - A MockApiConsumer instance
    consumer = mock_api_consumer_for_exceptions(base_url="https://example.com")

    # THEN - A RequestError should be raised when _make_request is called
    with pytest.raises(UnexcpectedError) as excinfo:
        consumer.get("api/test")

    # AND - The correct message should be displayed
    assert (
        str(excinfo.value)
        == "Unexcpected error: An unexpected error occurred: Generic request error"
    )
