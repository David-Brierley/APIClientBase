from .fixtures.pagination import mock_api_consumer, mock_api_consumer_all
from api_client_base.core.api_consumer import ApiConsumer
from api_client_base.core.paginator_offset import OffsetPaginator

"""
These tests are for the OffsetPaginator class. which is an implementation of the ApiPaginator class.
These specifically test the pagination functionality of the OffsetPaginator class and the all method.
"""


def test_offset_paginator(mock_api_consumer):
    # Given - a mock API consumer
    consumer = mock_api_consumer("https://test.com")

    # GIVEN - a paginator with a size of 100
    paginator = OffsetPaginator(size_value=100)

    # WITH - a path and method
    path = "/test"
    method = "GET"

    # THEN - the initial parameters should be set
    results = []

    # WHEN - paginating through the results
    for page in paginator.paginate(consumer, method, path):
        results.extend(page["items"])

    # THEN - the results should be paginated length should be 1000
    assert len(results) == 1000

    # THEN - the first item should have an id of 0
    assert results[0]["id"] == 0

    # THEN - the nth item should have an id of n
    assert results[500]["id"] == 500

    # THEN - the last item should have an id of 999
    assert results[-1]["id"] == 999


def test_offset_paginator_all(mock_api_consumer_all):
    # Given - a mock API consumer
    consumer = mock_api_consumer_all("https://test.com")

    # GIVEN - a paginator with a size of 100
    paginator = OffsetPaginator(
        size_value=100, offset_param="offset", total_key="total", items_key="items"
    )

    # WITH - a path and method
    path = "/test"
    method = "GET"

    # WHEN - paginating through the results
    all_results = paginator.all(consumer, method, path)

    # THEN - the results should be paginated length should be 1000
    assert len(all_results) == 1000

    # THEN - the first item should have an id of 0
    assert all_results[0]["id"] == 0

    # THEN - the nth item should have an id of n
    assert all_results[500]["id"] == 500
