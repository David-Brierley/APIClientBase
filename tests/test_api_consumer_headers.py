from api_client_base.core.api_consumer import ApiConsumer
from .fixtures.common import (
    mock_api_consumer_using_base_helpers,
    mock_api_consumer_update_headers,
)

"""
These test cases are for the headers functionality of the ApiConsumer Base Class.
they specifically test the update_headers method and the default headers.
"""


def test_default_headers(mock_api_consumer_using_base_helpers):
    # GIVEN - A TestApiConsumer instance
    consumer = mock_api_consumer_using_base_helpers("https://example.com")

    # THEN - The default headers should be set
    assert consumer.headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def test_custom_headers_additional(mock_api_consumer_using_base_helpers):
    # GIVEN - A TestApiConsumer instance
    consumer = mock_api_consumer_using_base_helpers("https://example.com")

    # WHEN - Custom headers are set after initialization
    consumer.update_headers({"Authorization": "Bearer token"})

    # THEN - The custom headers should be set
    assert consumer.headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer token",
    }


def test_subclass_with_headers_on_construct(mock_api_consumer_update_headers):
    # GIVEN - instance level headers
    instance_level_headers = {
        "Authorization": "sdasdasd",
    }
    # GIVEN - A TestApiConsumer instance

    # WHEN - Custom headers are set on initialization
    consumer = mock_api_consumer_update_headers(
        "https://example.com", instance_level_headers
    )

    # THEN - The custom headers should be set
    assert consumer.headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "sdasdasd",
    }
