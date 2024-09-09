import pytest
import json
import hashlib
from unittest.mock import patch
import time
from api_client_base.implementations.logicmonitor import LogicMonitorClient

"""
These test cases are for the LogicMonitorClient class.
WHich is a subclass of the ApiConsumer Base Class.
They test the initialization, the methods, and the headers functionality.
Additionally, they test the abstracted methods and the prepare_request decorator specifically.
These methods are unique to the LogicMonitorClient class.
"""


class TestLogicMonitorClient:
    @pytest.fixture
    def pylogicmonitor(self):
        # Return a LogicMonitorClient instance with test values
        return LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

    def test_initialization(self, pylogicmonitor):
        # GIVEN - A LogicMonitorClient instance

        # THEN - The base_url should be set correctly
        assert (
            pylogicmonitor.base_url
            == "https://testcompany.logicmonitor.com/santaba/rest"
        )

        # THEN - The access_id, api_key, and api_version should be set correctly
        assert pylogicmonitor.access_id == "testid"
        assert pylogicmonitor.api_key == "testkey"
        assert pylogicmonitor.api_version == 3

        # THEN - The headers should be set correctly
        assert pylogicmonitor.headers == {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Version": "3",
        }

    def test_calculate_epoch(self, pylogicmonitor):
        # GIVEN - A LogicMonitorClient instance

        # WHEN - We call the _calculate_epoch method
        epoch_time = pylogicmonitor._calculate_epoch()

        # THEN - The epoch time should be a string
        assert isinstance(epoch_time, str), "The epoch time should be a string."

        # THEN - The epoch time should be convertible to an integer
        try:
            epoch_time_int = int(epoch_time)
        except ValueError:
            pytest.fail("The epoch time should be convertible to an integer.")

        # THEN - The epoch time should be within 1 second of the current time
        current_time = int(time.time() * 1000)
        assert (
            abs(current_time - epoch_time_int) < 1000
        ), "The epoch time should be within 1 second of the current time."

    @patch.object(
        LogicMonitorClient, "_calculate_epoch", return_value=1625254875000
    )  # Mock epoch value
    def test_format_request_vars_get(self, mock_epoch, pylogicmonitor):
        # GIVEN - A LogicMonitorClient instance

        # WHEN - We call the _format_request_vars method with a GET request
        method = "GET"
        path = "api/v1/resource"
        payload = {}

        formatted_vars = pylogicmonitor._format_request_vars(method, path, payload)

        # THEN - The formatted request variables should be correct
        expected_string = f"{method}{mock_epoch.return_value}/{path}"
        expected_epoch = mock_epoch.return_value

        # THEN - The formatted request variables should be correct
        assert formatted_vars == (
            expected_string,
            expected_epoch,
        ), "The formatted request variables for GET are incorrect."

    @patch.object(
        LogicMonitorClient, "_calculate_epoch", return_value=1625254875000
    )  # Mock epoch value
    def test_format_request_vars_post(self, mock_epoch, pylogicmonitor):
        # GIVEN - A LogicMonitorClient instance

        # WHEN - We call the _format_request_vars method with a POST request
        method = "POST"
        path = "api/v1/resource"
        payload = {"key": "value"}

        formatted_vars = pylogicmonitor._format_request_vars(method, path, payload)

        # THEN - The formatted request variables should be correct
        expected_string = (
            f"{method}{mock_epoch.return_value}{json.dumps(payload)}{path}"
        )
        expected_epoch = mock_epoch.return_value

        # THEN - The formatted request variables should be correct
        assert formatted_vars == (
            expected_string,
            expected_epoch,
        ), "The formatted request variables for POST are incorrect."

    @patch("hmac.new")
    @patch("base64.b64encode")
    def test_construct_signature(self, mock_b64encode, mock_hmac_new, pylogicmonitor):
        # GIVEN - A LogicMonitorClient instance

        # GIVEN - Test values
        request_vars = "GET1625254875000/api/v1/resource"
        expected_digest = "abcdef1234567890"  # Example hex digest
        expected_base64_signature = (
            "YWJjZGVmMTIzNDU2Nzg5MA=="  # Example Base64 encoded string
        )

        # WHEN - We mock the hmac.new and base64.b64encode functions
        mock_hmac = mock_hmac_new.return_value
        mock_hmac.hexdigest.return_value = expected_digest
        mock_b64encode.return_value = expected_base64_signature.encode("utf-8")

        # WHEN - We call the _construct_signature method
        signature = pylogicmonitor._construct_signature(request_vars)

        # THEN - The signature should be correct
        assert (
            signature == expected_base64_signature
        ), "The constructed signature is incorrect."

        # THEN - hmac.new should be called with the correct parameters
        mock_hmac_new.assert_called_once_with(
            pylogicmonitor.api_key.encode("utf-8"),
            msg=request_vars.encode("utf-8"),
            digestmod=hashlib.sha256,
        )

        # THEN - base64.b64encode should be called with the correct parameters
        mock_b64encode.assert_called_once_with(expected_digest.encode("utf-8"))

    def test_construct_headers(self, pylogicmonitor):
        # GIVEN - An instance of LogicMonitorClient with specific access_id and api_key.

        # GIVEN - A predefined signature and epoch time to test the header construction.
        signature = "YWJjZGVmMTIzNDU2Nzg5MA=="
        epoch = "1625254875000"

        # EXPECTED - The expected headers dictionary based on the predefined signature and epoch
        expected_headers = {
            "Authorization": f"LMv1 {pylogicmonitor.access_id}:{signature}:{epoch}"
        }

        # WHEN - The _construct_headers method is called with the predefined signature and epoch time.
        headers = pylogicmonitor._construct_headers(signature, epoch)

        # THEN - The headers dictionary should match the expected headers dictionary.
        assert headers == expected_headers, "The constructed headers are incorrect."

    @patch.object(LogicMonitorClient, "_format_request_vars")
    @patch.object(LogicMonitorClient, "_construct_signature")
    @patch.object(LogicMonitorClient, "_construct_headers")
    @patch.object(LogicMonitorClient, "update_headers")
    @patch.object(LogicMonitorClient, "common_get")
    def test_prepare_request_decorator(
        self,
        mock_common_get,
        mock_update_headers,
        mock_construct_headers,
        mock_construct_signature,
        mock_format_request_vars,
        pylogicmonitor,
    ):
        # GIVEN
        # Define mock returns for _format_request_vars, _construct_signature, and _construct_headers
        mock_format_request_vars.return_value = (
            "GET1625254875000/some/path",
            "1625254875000",
        )
        mock_construct_signature.return_value = "signature"
        mock_construct_headers.return_value = {
            "Authorization": "LMv1 testid:signature:1625254875000"
        }

        # Define the path and kwargs for the test
        path = "some/path"
        kwargs = {"json": {}}

        # WHEN
        # Call the decorated method
        pylogicmonitor.get(path, **kwargs)

        # THEN
        # Check that _format_request_vars was called with 'GET', 'some/path', and {}
        mock_format_request_vars.assert_called_once_with(
            "GET", path, kwargs.get("json")
        )

        # Check that _construct_signature was called with the correct request_vars
        mock_construct_signature.assert_called_once_with("GET1625254875000/some/path")

        # Check that _construct_headers was called with the correct signature and epoch
        mock_construct_headers.assert_called_once_with("signature", "1625254875000")

        # Check that update_headers was called with the correct headers
        mock_update_headers.assert_called_once_with(
            {"Authorization": "LMv1 testid:signature:1625254875000"}
        )

        # Check that the decorated method (common_get) was called with the correct arguments
        mock_common_get.assert_called_once_with(path, **kwargs)

    # test abstracted methods
    @patch.object(LogicMonitorClient, "common_post")
    def test_post_method_calls_common_post(self, mock_common_post):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_common_post.return_value = {"status": "success"}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the post method
        response = pylogicmonitor.post("/test-path", json={"key": "value"})

        # THEN: Ensure the common_post method is called with the correct arguments
        mock_common_post.assert_called_once_with("/test-path", json={"key": "value"})
        # AND: Check that the response is what we mocked
        assert response == {"status": "success"}

    @patch.object(LogicMonitorClient, "common_put")
    def test_put_method_calls_common_put(self, mock_common_put):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_common_put.return_value = {"status": "success"}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the put method
        response = pylogicmonitor.put("/test-path", json={"key": "value"})

        # THEN: Ensure the common_put method is called with the correct arguments
        mock_common_put.assert_called_once_with("/test-path", json={"key": "value"})
        # AND: Check that the response is what we mocked
        assert response == {"status": "success"}

    @patch.object(LogicMonitorClient, "common_patch")
    def test_patch_method_calls_common_patch(self, mock_common_patch):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_common_patch.return_value = {"status": "success"}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the patch method
        response = pylogicmonitor.patch("/test-path", json={"key": "value"})

        # THEN: Ensure the common_patch method is called with the correct arguments
        mock_common_patch.assert_called_once_with("/test-path", json={"key": "value"})
        # AND: Check that the response is what we mocked
        assert response == {"status": "success"}

    @patch.object(LogicMonitorClient, "common_delete")
    def test_delete_method_calls_common_delete(self, mock_common_delete):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_common_delete.return_value = {"status": "success"}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the delete method
        response = pylogicmonitor.delete("/test-path")

        # THEN: Ensure the common_delete method is called with the correct arguments
        mock_common_delete.assert_called_once_with("/test-path")
        # AND: Check that the response is what we mocked
        assert response == {"status": "success"}

    @patch.object(LogicMonitorClient, "common_get")
    def test_get_method_calls_common_get(self, mock_common_get):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_common_get.return_value = {"status": "success"}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the get method
        response = pylogicmonitor.get("/test-path")

        # THEN: Ensure the common_get method is called with the correct arguments
        mock_common_get.assert_called_once_with("/test-path")
        # AND: Check that the response is what we mocked
        assert response == {"status": "success"}

    @patch.object(LogicMonitorClient, "get")
    def test_count_method_calls_get(self, mock_get):
        # GIVEN: Setup the LogicMonitorClient instance
        mock_get.return_value = {"total": 10}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the count method
        count = pylogicmonitor.count("/test-path")

        # THEN: Ensure the get method is called with the correct arguments
        mock_get.assert_called_once_with(
            "/test-path", params={"fields": "id", "size": 1}
        )
        # AND: Check that the count is what we mocked
        assert count == 10

    @patch.object(LogicMonitorClient, "get")
    def test_count_method_calls_get_and_overrides_params_size_and_field(self, mock_get):
        params = {"size": 1000, "fields": "id,displayName"}

        # GIVEN: Setup the LogicMonitorClient instance
        mock_get.return_value = {"total": 10}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # WHEN: Call the count method
        count = pylogicmonitor.count("/test-path", params=params)

        # THEN: Ensure the get method is called with the correct arguments, size should be 1 and fields should be id regardless of the params passed
        mock_get.assert_called_once_with(
            "/test-path", params={"fields": "id", "size": 1}
        )
        # AND: Check that the count is what we mocked
        assert count == 10

    @patch.object(LogicMonitorClient, "get")
    def test_count_method_calls_get_and_preserves_additional_params(self, mock_get):

        # GIVEN: Setup the LogicMonitorClient instance
        mock_get.return_value = {"total": 10}
        pylogicmonitor = LogicMonitorClient(
            company="testcompany", access_id="testid", api_key="testkey"
        )

        # GIVEN: Additional params
        params = {"size": 1000, "fields": "id,displayName", "filter": "name:test"}

        # WHEN: Call the count method
        count = pylogicmonitor.count("/test-path", params=params)

        # THEN: Ensure the get method is called with the correct arguments, extra params should be preserved
        mock_get.assert_called_once_with(
            "/test-path", params={"fields": "id", "size": 1, "filter": "name:test"}
        )
        # AND: Check that the count is what we mocked
        assert count == 10
