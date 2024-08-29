class APIException(Exception):
    """Base class for all API-related exceptions."""

    pass


class HTTPError(APIException):
    """Exception raised for HTTP errors."""

    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"Request Error: Request to URL failed with HTTP code {self.status_code}: {self.message}"


class ConnectionError(APIException):
    """Exception raised for connection-related errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Connection error: {self.message}"


class TimeoutError(APIException):
    """Exception raised for request timeouts."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Request timed out: {self.message}"


class RequestError(APIException):
    """Exception raised for general request errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Request error: {self.message}"


class UnexcpectedError(APIException):
    """Exception raised for general request errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Unexcpected error: {self.message}"
