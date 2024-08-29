import pytest
from pydantic import ValidationError
from api_client_base.models.base_url import BaseURL

"""
These tests are for the BaseURL model ensuring that the URL validation works as expected.
"""

valid_urls = [
    "http://example.com",  # Valid URL http
    "https://example.com",  # Valid URL https
    "https://subdomain.example.com",  # Valid URL with subdomain
    "http://example.com/path",  # Valid URL with path
    "http://example.com:8080",  # Valid URL with port
]

invalid_urls = (
    [
        "ftp://example.com",  # Invalid scheme
        "www.example.com",  # Missing scheme
        "example.com",  # Missing scheme
        "http:/example.com",  # Malformed scheme
        "://example.com",  # Missing scheme and host
    ],
)


# Test valid URLs
@pytest.mark.parametrize("valid_url", valid_urls)
def test_valid_urls(valid_url):
    # Given - a valid URL
    url_model = BaseURL(url=valid_url)
    # Then - the URL should be set correctly
    assert url_model.url == valid_url


# Test invalid URLs
@pytest.mark.parametrize("invalid_url", invalid_urls)
def test_invalid_urls(invalid_url):
    # Given - an invalid URL

    # Then - a validation error should be raised
    with pytest.raises(ValidationError):
        BaseURL(url=invalid_url)
