import pytest
from api_client_base.core.api_consumer import ApiConsumer


class MockApiConsumerForExceptions(ApiConsumer):
    def get(self, path: str, **kwargs):
        # needs to implement _make_request to ensure exceptions are raised when called
        return self._make_request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        pass

    def put(self, path: str, **kwargs):
        pass

    def patch(self, path: str, **kwargs):
        pass

    def delete(self, path: str, **kwargs):
        pass

    def update_headers(self, headers: dict):
        pass


@pytest.fixture
def mock_api_consumer_for_exceptions():
    return MockApiConsumerForExceptions
