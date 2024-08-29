import pytest
from unittest.mock import patch
from api_client_base.implementations.basic_token import BasicTokenClient

"""
These test cases are for the BasicTokenClient class.
WHich is a subclass of the ApiConsumer Base Class.
They test the initialization, the methods, and the headers functionality.
"""


class TestLogicMonitorClient:
    @pytest.fixture
    def basic_token_client_default_header(self):
        # Return an instance of BasicTokenClient for testing
        return BasicTokenClient(base_path="example.com/api/v1", api_key="mYApiK3Y12")

    @pytest.fixture
    def basic_token_client_different_header(self):
        # Return an instance of BasicTokenClient for testing
        return BasicTokenClient(
            base_path="example.com/api/v1",
            api_key="mYApiK3Y12",
            api_header="X-MyApiHeaderThing",
        )

    def test_initialization_default_header(self, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance with default values

        # THEN - The base_url should be set correctly
        assert (
            basic_token_client_default_header.base_url == "https://example.com/api/v1"
        )

        # THEN - The headers should be set correctly
        assert basic_token_client_default_header.headers == {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-APIKey": "mYApiK3Y12",
        }

    def test_initialization_different_header(self, basic_token_client_different_header):
        # GIVEN - A BasicTokenClient instance with a different header

        # THEN - The base_url should be set correctly
        assert (
            basic_token_client_different_header.base_url == "https://example.com/api/v1"
        )

        # THEN - The headers should be set correctly
        assert basic_token_client_different_header.headers == {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-MyApiHeaderThing": "mYApiK3Y12",
        }

    @patch("api_client_base.implementations.basic_token.ApiConsumer.common_get")
    def test_get_method(self, mock_common_get, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance

        # WHEN - The get method is called
        basic_token_client_default_header.get("/test")

        # THEN - The common_get method should be called
        mock_common_get.assert_called_once_with("/test")

    @patch("api_client_base.implementations.basic_token.ApiConsumer.common_post")
    def test_post_method(self, mock_common_post, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance

        # WHEN - The post method is called
        basic_token_client_default_header.post("/test")

        # THEN - The common_post method should be called
        mock_common_post.assert_called_once_with("/test")

    @patch("api_client_base.implementations.basic_token.ApiConsumer.common_put")
    def test_put_method(self, mock_common_put, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance

        # WHEN - The put method is called
        basic_token_client_default_header.put("/test")

        # THEN - The common_put method should be called
        mock_common_put.assert_called_once_with("/test")

    @patch("api_client_base.implementations.basic_token.ApiConsumer.common_patch")
    def test_patch_method(self, mock_common_patch, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance

        # WHEN - The patch method is called
        basic_token_client_default_header.patch("/test")

        # THEN - The common_patch method should be called
        mock_common_patch.assert_called_once_with("/test")

    @patch("api_client_base.implementations.basic_token.ApiConsumer.common_delete")
    def test_delete_method(self, mock_common_delete, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance

        # WHEN - The delete method is called
        basic_token_client_default_header.delete("/test")

        # THEN - The common_delete method should be called
        mock_common_delete.assert_called_once_with("/test")

    def test_update_headers(self, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance with initial headers

        # WHEN - The update_headers method is called with new headers
        new_headers = {"X-New-Header": "NewValue"}
        basic_token_client_default_header.update_headers(new_headers)

        # THEN - The headers should include the new header
        expected_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-APIKey": "mYApiK3Y12",
            "X-New-Header": "NewValue",
        }

        # THEN - The headers should include the new header
        assert basic_token_client_default_header.headers == expected_headers

    def test_override_headers(self, basic_token_client_default_header):
        # GIVEN - A BasicTokenClient instance with initial headers

        # WHEN - The headers are updated directly
        new_headers = {"Content-Type": "application/xml"}
        basic_token_client_default_header.headers.update(new_headers)

        # THEN - The headers default header of json should be overridden
        expected_headers = {
            "Content-Type": "application/xml",
            "Accept": "application/json",
            "X-APIKey": "mYApiK3Y12",
        }

        # THEN - The headers should include the new header
        assert basic_token_client_default_header.headers == expected_headers
