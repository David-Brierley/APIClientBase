import json
import hashlib
import base64
import time
import hmac
import functools

from api_client_base.core.api_consumer import ApiConsumer
from api_client_base.core.paginator_offset import OffsetPaginator


class LogicMonitorClient(ApiConsumer, OffsetPaginator):
    """
    LogicMonitor API consumer class that extends the base API consumer and the OffsetPaginator.
    This class handles the LogicMonitor API requests and pagination.
    """

    size_param = "size"  # The parameter to set the size of the page
    size_value = 100  # The default size value
    offset_param = "offset"  # The parameter to set the offset of the page
    total_key = (
        "total"  # The key in the response that contains the total number of items
    )
    items_key = "items"  # The key in the response that contains the items

    def __init__(self, company, api_key: str, access_id: str, api_version: int = 3):
        """
        Initializes the Logicmonitor API consumer with the required credentials.

        Args:
            company (str): The company name for the Logicmonitor account.
            api_key (str): The API key for the Logicmonitor account.
            access_id (str): The access ID for the Logicmonitor account.
            api_version (int, optional): The API version to use. Defaults to 3.
        """

        base_url = f"https://{company}.logicmonitor.com/santaba/rest"
        self.api_key = api_key
        self.access_id = access_id
        self.api_version = api_version
        headers = {"X-Version": str(api_version)}
        super().__init__(base_url, headers=headers)

    @staticmethod
    def prepare_request(func):
        """
        Decorator to prepare the request before calling the actual request method.
        Calculates the epoch time, formats the request variables, constructs the signature, and updates the headers.

        Args:
            func: The original request method.

        Returns:
            function: The wrapper function that prepares the request before calling the original method.
        """

        @functools.wraps(func)
        def wrapper(self, path: str, **kwargs) -> dict:
            method = func.__name__.upper()
            payload = kwargs.get("json", {})

            # Call the _prepare_for_request logic
            request_vars, epoch = self._format_request_vars(method, path, payload)
            signature = self._construct_signature(request_vars)
            headers = self._construct_headers(signature, epoch)
            self.update_headers(headers)

            return func(self, path, **kwargs)

        return wrapper

    @prepare_request
    def get(self, path: str, all: bool = False, **kwargs) -> dict:
        """
        Handle GET requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the GET request.

        Returns:
            dict: The JSON response from the API.
        """
        return (
            self.all(self, "GET", path, **kwargs)
            if all
            else self.common_get(path, **kwargs)
        )

    @prepare_request
    def post(self, path: str, **kwargs) -> dict:
        """
        Handle POST requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the POST request.

        Returns:
            dict: The JSON response from the API.
        """
        return self.common_post(path, **kwargs)

    @prepare_request
    def put(self, path: str, **kwargs) -> dict:
        """
        Handle PUT requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PUT request.

        Returns:
            dict: The JSON response from the API.
        """
        return self.common_put(path, **kwargs)

    @prepare_request
    def patch(self, path: str, **kwargs) -> dict:
        """
        Handle PATCH requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PATCH request.

        Returns:
            dict: The JSON response from the API.
        """
        return self.common_patch(path, **kwargs)

    @prepare_request
    def delete(self, path: str, **kwargs) -> dict:
        """
        Handle DELETE requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the DELETE request.

        Returns:
            dict: The JSON response from the API.
        """
        return self.common_delete(path, **kwargs)

    def update_headers(self, headers: dict) -> None:
        """
        Update the headers for the request.

        Args:
            headers (dict): The headers to update.

        Returns:
            None
        """
        self.headers.update(headers)

    def _calculate_epoch(self) -> int:
        """
        Calculate the epoch time (required for the signature)

        Returns:
            int: The epoch time
        """
        return str(int(time.time() * 1000))

    def _format_request_vars(self, method: str, path: str, payload: dict = {}) -> tuple:
        """
        Format the request variables (required for the signature)

        Args:
            method: (str): The request method
            path: (str): The request path
            payload: (dict): The request payload

        Returns:
            tuple: The formatted request variables (str, epoch)
        """
        epoch = self._calculate_epoch()

        if method == "GET":
            request_vars = f"{method}{epoch}/{path}"
        else:
            payload_str = json.dumps(payload)
            request_vars = f"{method}{epoch}{payload_str}{path}"

        return request_vars, epoch

    def _construct_signature(self, request_vars: str) -> str:
        """
        Constructs the standard LM signature required to build the headers
        Args:
            request_vars: (str): the str formatted request vars constructed by _format_request_vars

        Returns:
            str: string object that represents the Base64-encoded digest string.
        """
        digest = hmac.new(
            self.api_key.encode("utf-8"),
            msg=request_vars.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        signature = base64.b64encode(digest.encode("utf-8")).decode("utf-8")
        return signature

    def _construct_headers(self, signature: str, epoch: str) -> dict:
        """
        Constructs the standard LM headers for the request
        Args:
            signature: (str): the signature which should have been generated using _construct_signature
            epoch: (str): the epoch is rturned as a tuple from _format_request_vars, this is the epoch time

        Returns:
            dict: The dictionary of headers for the request (Sepcifically the Authorization header)
        """
        return {"Authorization": f"LMv1 {self.access_id}:{signature}:{epoch}"}
