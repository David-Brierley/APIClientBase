from abc import ABC, abstractmethod
import urllib.parse
from api_client_base.core.api_consumer import ApiConsumer


class ApiPaginator(ABC):
    """
    Base class for handling pagination in API requests based on URL parameters.

    Subclasses should implement the logic for different pagination schemes (e.g., page number, offset-based).
    """

    def __init__(self, size_param: str = "size", size_value: int = 10):
        self.size_param = size_param
        self.size_value = size_value

    @abstractmethod
    def get_next_params(self, response, current_params: dict) -> dict:
        """
        Abstract method to determine the parameters for the next page.

        Args:
            response: The response object from the current page request.
            current_params (dict): The current URL parameters.

        Returns:
            dict: The parameters for the next page, or None if there are no more pages.
        """
        pass  # pragma: no cover

    @abstractmethod
    def all(self, consumer: "ApiConsumer", method: str, path: str, **kwargs) -> list:
        """
        Method to fetch all pages of results.

        Args:
            consumer (ApiConsumer): The API consumer instance.
            method (str): The HTTP method (GET, POST, etc.).
            path (str): The API endpoint path.
            kwargs: Additional arguments for the request, including initial URL params.

        Returns:
            list: The combined data from all pages.
        """
        pass  # pragma: no cover

    def paginate(self, consumer: "ApiConsumer", method: str, path: str, **kwargs):
        """
        Generator to paginate through API results.

        Args:
            consumer (ApiConsumer): The API consumer instance.
            method (str): The HTTP method (GET, POST, etc.).
            path (str): The API endpoint path.
            kwargs: Additional arguments for the request, including initial URL params.

        Yields:
            The data from each page until there are no more pages.
        """
        params = kwargs.pop("params", {})
        params[self.size_param] = self.size_value

        while params:
            # Merge the base URL with the parameters
            query_string = urllib.parse.urlencode(params)
            full_path = f"{path}?{query_string}"

            response = consumer._make_request(method, full_path, **kwargs)
            yield response

            params = self.get_next_params(response, params)
