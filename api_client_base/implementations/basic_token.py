from api_client_base.core.api_consumer import ApiConsumer


class BasicTokenClient(ApiConsumer):
    def __init__(self, base_path: str, api_key: str, api_header: str = "X-APIKey"):
        """
        Minimal implementation of an API client using a basic token.
        e.g. an API which only requires an API key in the headers.

        Args:
            base_path (str): The base path for the API.
            api_key (str): The API key for the API.
            api_header (str, optional): The header to use for the API key. Defaults to "X-APIKey".
        """

        base_url = f"https://{base_path}"
        headers = {api_header: api_key}
        super().__init__(base_url, headers=headers)

    def get(self, path: str, **kwargs) -> dict:
        """
        Handle GET requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the GET request.

        Returns:
            dict: The JSON response from the API.
        """
        return self.common_get(path, **kwargs)

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
