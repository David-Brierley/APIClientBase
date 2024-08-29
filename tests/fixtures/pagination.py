import pytest
from api_client_base.core.api_consumer import ApiConsumer
import urllib.parse

"""
Mock subclasses of ApiConsumer specifically for testing pagination.
"""


class MockApiConsumer(ApiConsumer):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str, **kwargs):
        pass

    def post(self, path: str, **kwargs):
        pass

    def put(self, path: str, **kwargs):
        pass

    def delete(self, path: str, **kwargs):
        pass

    def patch(self, path: str, **kwargs):
        pass

    def update_headers(self, headers: dict):
        pass

    def _make_request(self, method: str, path: str, **kwargs):
        """
        This method will be called internally by the helper (paginate) in APIPaginator
        We simulate a paginated API response here.
        """
        # simulate multiple pages of results
        query_string = urllib.parse.urlparse(path).query
        params = urllib.parse.parse_qs(query_string)
        offset = int(params.get("offset", [0])[0])
        size = int(params.get("size", [10])[0])

        total = 1000
        items = [{"id": i, "name": f"Item {i}"} for i in range(offset, offset + size)]

        return {"total": total, "items": items}


class MockApiConsumerAll(ApiConsumer):
    size_param = "size"
    size_value = 100
    offset_param = "offset"
    total_key = "total"
    items_key = "items"

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str, **kwargs):
        pass

    def post(self, path: str, **kwargs):
        pass

    def put(self, path: str, **kwargs):
        pass

    def delete(self, path: str, **kwargs):
        pass

    def patch(self, path: str, **kwargs):
        pass

    def update_headers(self, headers: dict):
        pass

    def _make_request(self, method: str, path: str, **kwargs):
        """
        This method will be called internally by the abstract method in OffsetPaginator
        We simulate a paginated API response here.
        """
        # get parameters from params dict
        params = kwargs.get("params", {})
        offset = int(params.get("offset", 0))
        size = int(params.get("size", 100))
        print(size)

        total = 1000
        items = [{"id": i, "name": f"Item {i}"} for i in range(offset, offset + size)]

        return {"total": total, "items": items}


@pytest.fixture
def mock_api_consumer():
    """
    return a mock API consumer for testing pagination
    """
    return MockApiConsumer


@pytest.fixture
def mock_api_consumer_all():
    """
    return a mock API consumer for testing pagination (all method)
    """
    return MockApiConsumerAll
