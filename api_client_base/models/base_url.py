import re
from pydantic import BaseModel, validator


class BaseURL(BaseModel):
    """
    Base URL model for API consumer.

    Attributes:
        url (str): The base URL for the API.
    """

    url: str

    @validator("url")
    def validate_base_url(cls, v):
        """
        Validate the base URL.

        Args:
            v (str): The base URL.

        Returns:
            str: The validated base URL.
        """
        if not re.match(r"^https?://", v):
            raise ValueError("Invalid URL")
        return v
