from abc import ABC, abstractmethod
import requests
from api_client_base.models.base_url import BaseURL
from api_client_base.core.exceptions import (
    HTTPError,
    ConnectionError,
    TimeoutError,
    RequestError,
    UnexcpectedError,
)


class ApiConsumer(ABC):
    """
    Abstract base class for API consumers.

    This class provides a structure for making HTTP requests to an API with a base URL and common headers.
    Subclasses should implement the specific methods for different HTTP methods (GET, POST, PUT, PATCH, DELETE).
    Additional headers & individual logic such as authentication can be implemented in the subclass.
    """

    def __init__(self, base_url: str, headers: dict = None):
        """
        Initializes the ApiConsumer with a base URL and optional headers.

        Args:
            base_url (str): The base URL for the API.
            headers (dict, optional): Additional headers to include in all requests. Defaults to common headers.
        """
        base_url = BaseURL(url=base_url)
        self.base_url = base_url.url

        # Common headers for all requests
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if headers:
            self.headers.update(headers)

    @abstractmethod
    def get(self, path: str, **kwargs):
        """
        Abstract method for handling GET requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the GET request.

        This method must be implemented by subclasses.
        """
        pass  # pragma: no cover

    @abstractmethod
    def post(self, path: str, **kwargs):
        """
        Abstract method for handling POST requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the POST request.

        This method must be implemented by subclasses.
        """
        pass  # pragma: no cover

    @abstractmethod
    def put(self, path: str, **kwargs):
        """
        Abstract method for handling PUT requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PUT request.

        This method must be implemented by subclasses.
        """
        pass  # pragma: no cover

    @abstractmethod
    def patch(self, path: str, **kwargs):
        """
        Abstract method for handling PATCH requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PATCH request.

        This method must be implemented by subclasses.
        """
        pass  # pragma: no cover

    @abstractmethod
    def delete(self, path: str, **kwargs):
        """
        Abstract method for handling DELETE requests.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the DELETE request.

        This method must be implemented by subclasses.
        """
        pass  # pragma: no cover

    def _make_request(self, method: str, path: str, **kwargs):
        """
        Internal method for making an HTTP request.

        Args:
            method (str): The HTTP method (GET, POST, PUT, PATCH, DELETE).
            path (str): The API endpoint path.
            kwargs: Additional arguments for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            HTTPError: If the HTTP request returns an unsuccessful status code.
        """
        url = f"{self.base_url}/{path}"
        # Ensure headers are included in the request
        headers = kwargs.pop("headers", {})
        headers.update(self.headers)
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPError(response.status_code, str(http_err))
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Connection error occurred when trying to reach {url}"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request to {url} timed out")
        except requests.exceptions.RequestException as req_err:
            raise RequestError(f"Request error occurred: {str(req_err)}")
        except Exception as err:
            raise UnexcpectedError(f"An unexpected error occurred: {str(err)}")
        return response.json()

    @abstractmethod
    def update_headers(self, headers: dict):
        """
        Abstract method for updating headers.

        Args:
            headers (dict): A dictionary of headers to update.

        This method must be implemented by subclasses.
        """
        self.headers.update(headers)

    def common_get(self, path: str, **kwargs):
        """
        Wrapper method for making a GET request.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the GET request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._make_request("GET", path, **kwargs)

    def common_post(self, path: str, **kwargs):
        """
        Wrapper method for making a POST request.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the POST request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._make_request("POST", path, **kwargs)

    def common_put(self, path: str, **kwargs):
        """
        Wrapper method for making a PUT request.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PUT request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._make_request("PUT", path, **kwargs)

    def common_patch(self, path: str, **kwargs):
        """
        Wrapper method for making a PATCH request.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the PATCH request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._make_request("PATCH", path, **kwargs)

    def common_delete(self, path: str, **kwargs):
        """
        Wrapper method for making a DELETE request.

        Args:
            path (str): The API endpoint path.
            kwargs: Additional arguments for the DELETE request.

        Returns:
            dict: The JSON response from the API.
        """
        return self._make_request("DELETE", path, **kwargs)
