from api_client_base.core.api_paginator import ApiPaginator
from api_client_base.core.api_consumer import ApiConsumer
from typing import Union


class OffsetPaginator(ApiPaginator):
    """
    A Paginator implementation for offset-based pagination.
    e.g. ?offset=0&size=10

    Args:
        offset_param (str): The URL parameter name for the offset. Defaults to "offset".
        size_param (str): The URL parameter name for the page size. Defaults to "size".
        size_value (int): The default page size. Defaults to 10.
        total_key (str): The key in the response object that contains the total number of items. Defaults to "total".
    """

    def __init__(
        self,
        offset_param: str = "offset",
        size_param: str = "size",
        size_value: int = 10,
        total_key: str = "total",
        items_key: Union[str, None] = None,
    ):
        """
        Initializes the OffsetPaginator with the required parameters.

        Args:
            offset_param (str): The URL parameter name for the offset.
            size_param (str): The URL parameter name for the page size.
            size_value (int): The default page size.
            total_key (str): The key in the response object that contains the total number of items.
            items_key (Union[str, None]): The key in the response object that contains the items. Defaults to None.
        """
        super().__init__(size_param, size_value)
        self.offset_param = offset_param
        self.total_key = total_key
        self.items_key = items_key

    def get_next_params(self, response, current_params: dict) -> dict:
        """
        Updates the offset parameter for the next page.

        Args:
            response: The response object from the current page request.
            current_params (dict): The current URL parameters.

        Returns:
            dict: The parameters for the next page, or None if there are no more pages.
        """
        current_offset = current_params.get(self.offset_param, 0)
        total_items = response.get(self.total_key, 0)

        # Check if there are more items to fetch
        if current_offset + self.size_value >= total_items:
            return None

        # Update the offset for the next page
        next_offset = current_offset + self.size_value
        current_params[self.offset_param] = next_offset
        return current_params

    def all(self, consumer: "ApiConsumer", method: str, path: str, **kwargs) -> list:
        """
        Fetches all pages of results and combines them into a single list.
        If items_key is provided, it will be used to extract the items from the response.
        Otherwise, the entire response will be used as the items.

        Args:
            consumer (ApiConsumer): The API consumer instance.
            method (str): The HTTP method (GET, POST, etc.).
            path (str): The API endpoint path.
            kwargs: Additional arguments for the request, including initial URL params.

        Returns:
            list: The combined data from all pages.
        """
        all_results = []
        current_params = kwargs.pop("params", {})
        current_params[self.size_param] = self.size_value

        while current_params:
            response = consumer._make_request(
                method, path, params=current_params, **kwargs
            )
            # try to get the items from the response, or use the response itself if no items key is provided or found
            items = response.get(self.items_key, response)
            all_results.extend(items)
            current_params = self.get_next_params(response, current_params)

        return all_results
