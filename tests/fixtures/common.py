import pytest
from api_client_base.core.api_consumer import ApiConsumer


class MockApiConsumerBasic(ApiConsumer):
    """
    Test class to test basic functionality of Base Class
    """

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def get(self, path: str, **kwargs):
        return f"GET request to {self.base_url}{path}"

    def post(self, path: str, **kwargs):
        return f"POST request to {self.base_url}{path}"

    def put(self, path: str, **kwargs):
        return f"PUT request to {self.base_url}{path}"

    def patch(self, path: str, **kwargs):
        return f"PATCH request to {self.base_url}{path}"

    def delete(self, path: str, **kwargs):
        return f"DELETE request to {self.base_url}{path}"

    def update_headers(self, headers: dict):
        return super().update_headers(headers)


class MockApiConsumerUsingBaseHelpers(ApiConsumer):
    """
    test SubClass to test BaseClass functionality
    This subclass uses the helper methods from the BaseClass
    """

    def get(self, path: str, **kwargs):
        return self.common_get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.common_post(path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.common_put(path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self.common_patch(path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.common_delete(path, **kwargs)

    def update_headers(self, headers: dict):
        return super().update_headers(headers)


class MockApiConsumerUpdateHeaders(ApiConsumer):
    """
    Accepts headers in the constructor
    """

    def __init__(self, base_url: str, headers: dict = None):
        super().__init__(base_url, headers)

    def get(self, path: str, **kwargs):
        return self.common_get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.common_post(path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.common_put(path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self.common_patch(path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.common_delete(path, **kwargs)

    def update_headers(self, headers: dict):
        return super().update_headers(self.headers)


@pytest.fixture
def mock_api_consumer_basic():
    """
    return a mock API consumer for testing basic functionality
    """
    return MockApiConsumerBasic


@pytest.fixture
def mock_api_consumer_using_base_helpers():
    """
    return a mock API consumer for testing base class helper / wrapper methods
    """
    return MockApiConsumerUsingBaseHelpers


@pytest.fixture
def mock_api_consumer_update_headers():
    """
    return a mock API consumer for testing updating headers
    """
    return MockApiConsumerUpdateHeaders
