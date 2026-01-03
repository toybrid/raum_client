'''
© 2023 Arjun Thekkummadathil. All Rights Reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy of this 
text and associated documentation files (the "Text"), to deal in the Text without 
restriction, including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Text, and to permit persons 
to whom the Text is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Text.

THE TEXT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE TEXT OR THE USE OR OTHER DEALINGS IN THE TEXT.
'''
import os
import getpass
from typing import List
import requests
from raum_client.constants import DEFAULT_LIMIT, DEFAULT_OFFSET, DEFAULT_SORT

class Client:
    def __init__(self, host_url=None, port=None):
        self.base_url = os.getenv(
                                'RAUM_SERVER_BASE_URL', 
                                'http://localhost:8000/api/v1'
                                )
        if host_url and port:
            self.base_url = f"http://{host_url}:{port}/api/v1"

        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
        self.username = getpass.getuser()

    def _get(self, url, filters):
        """
        Sends a GET request to the specified URL with optional filters.

        Parameters:
        url (str): The URL to send the GET request to.
        filters (dict, optional): A dictionary of filters to apply to the request. Defaults to None.

        Returns:
        requests.Response: The response from the server.
        """
        resp = self.session.get(url, params=filters, headers=self.headers)
        if resp.status_code == 200:
            return resp
        else:
            raise ValueError(resp.text)


    def _post(self, url, payload, params=None):
        """
        Sends a POST request to the specified URL with a JSON payload and optional parameters.

        Parameters:
        url (str): The URL to send the POST request to.
        payload (dict): A dictionary representing the JSON payload to send with the request.
        params (dict, optional): A dictionary of parameters to send with the request. Defaults to None.

        Returns:
        requests.Response: The response from the server.
        """
        resp = self.session.post(url, json=payload, headers=self.headers, params=params)
        if resp.status_code in [201, 200]:
            return resp
        else:
            raise ValueError(resp.text)


    def _patch(self, url, payload=None):
        """
        Sends a PATCH request to the specified URL with a JSON payload.

        Parameters:
        url (str): The URL to send the PATCH request to.
        payload (dict, optional): A dictionary representing the JSON payload to send with the request. Defaults to None.

        Returns:
        requests.Response: The response from the server.
        """
        resp = self.session.patch(url, json=payload, headers=self.headers)
        if resp.status_code in [201, 200]:
            return resp
        else:
            raise ValueError(resp.text)

    def create(self, entity:str, fields: dict):
        """
        Creates a new entity with the specified fields.

        Args:
            entity (str): The name of the entity to create.
            fields (dict): A dictionary of fields and their values for the entity.

        Returns:
            dict: The JSON response from the API after creating the entity.

        Notes:
            Automatically adds 'created_by' and 'updated_by' fields using the current user.
        """

        default_fields = {
            "created_by": self.username,
            "updated_by": self.username,
        }
        payload = {
            "entity": entity,
            "fields": {**default_fields, **fields}
        }
        url = f"{self.base_url}/create"
        response = self._post(url, payload)
        return response.json()

    def search(self, entity: str, filters: dict = {}, fields: List[str] = [], sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Searches for entities based on specified filters, fields, sorting, and pagination.

        Args:
            entity (str): The name of the entity to search for.
            filters (dict, optional): Dictionary of filters to apply to the search. Defaults to {}.
            fields (List[str], optional): List of fields to include in the results. Defaults to [].
            sort (Any, optional): Sorting criteria for the results. Defaults to DEFAULT_SORT.
            limit (int, optional): Maximum number of results to return. Defaults to DEFAULT_LIMIT.
            offset (int, optional): Number of results to skip for pagination. Defaults to DEFAULT_OFFSET.

        Returns:
            List[dict]: A list of dictionaries representing the search results.
        """
        extended_fields = ['id']
        extended_fields.extend(fields)

        payload = {
            "entity": entity,
            "filters": filters,
            "fields": extended_fields,
            "sort": sort,
        }
        params = {
            "limit": limit,
            "offset": offset
            }
        url = f"{self.base_url}/search"
        response = self._post(url, payload, params=params)
        results = response.json()['items']
        return results
    
    def update(self, entity: str, uid: str, fields: dict):
        """
        Updates an entity with the specified fields.

        Args:
            entity (str): The name of the entity to update.
            uid (str): The unique identifier of the entity.
            fields (dict): A dictionary of fields to update with their new values.

        Returns:
            dict: The JSON response from the server after updating the entity.
        """
        default_fields = {
            "updated_by": self.username,
        }
        payload = {
            "entity": entity,
            "entity_id": str(uid),
            "fields": {**default_fields, **fields}
        }
        url = f"{self.base_url}/update"
        response = self._patch(url, payload)
        return response.json()
    
    def get_by_id(self, entity: str, uid: int, fields: List[str] = []):
        """
        Retrieves an entity by its unique identifier.

        Args:
            entity (str): The name of the entity to retrieve.
            uid (int): The unique identifier of the entity.

        Returns:
            dict: The JSON response from the server containing the entity data.
        """
        extended_fields = ['id']
        extended_fields.extend(fields)

        payload = {
            "entity": entity,
            "fields": extended_fields
        }
        url = f"{self.base_url}/get-by-id/{uid}"
        response = self._post(url, payload)
        return response.json()
    
    def create_bundle(self, fields: dict):
        """
        Creates a new bundle entity with the specified fields.

        This method constructs a payload containing the provided fields merged with default
        metadata fields (`created_by` and `updated_by` set to the current user), and sends
        a POST request to the backend to create a new bundle.

        Args:
            fields (dict): A dictionary of fields to include in the bundle entity.

        Returns:
            dict: The JSON response from the backend after creating the bundle.
        """
        user = getpass.getuser()

        default_fields = {
            "created_by": self.username,
            "updated_by": self.username,
        }
        payload = {
            "entity": "Bundle",
            "fields": {**default_fields, **fields}
        }
        url = f"{self.base_url}/create-bundle"
        response = self._post(url, payload)
        return response.json()
    
    def search_bundle(self, filters: dict = {}, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Searches for bundles using specified filters, sorting, and pagination options.

        Args:
            filters (dict, optional): Dictionary of filter criteria to apply to the search. Defaults to an empty dict.
            sort (str, optional): Sorting criteria for the search results. Defaults to DEFAULT_SORT.
            limit (int, optional): Maximum number of results to return. Defaults to DEFAULT_LIMIT.
            offset (int, optional): Number of results to skip before starting to collect the result set. Defaults to DEFAULT_OFFSET.

        Returns:
            list: A list of bundle items matching the search criteria.
        """
        payload = {
            "filters": filters,
            "sort": sort,
        }
        params = {
            "limit": limit,
            "offset": offset
            }
        url = f"{self.base_url}/search-bundle"
        response = self._post(url, payload, params=params)
        results = response.json()['items']
        return results
    

    def create_product_dependency(self, fields: dict):
        """
        Creates a new ProductDependency entity with the specified fields.

        This method constructs a payload with the provided fields, along with
        default 'created_by' and 'updated_by' fields set to the current user,
        and sends a POST request to the backend API to create the entity.

        Args:
            fields (dict): A dictionary of fields to set on the ProductDependency entity.

        Returns:
            dict: The JSON response from the API after creating the ProductDependency.
        """
        default_fields = {
            "created_by": self.username,
            "updated_by": self.username,
        }
        payload = {
            "entity": "ProductDependency",
            "fields": {**default_fields, **fields}
        }
        url = f"{self.base_url}/create-product-dependency"
        response = self._post(url, payload)
        return response.json()
    
    def get_product_dependency(self, uid):
        """
        Retrieve the dependency information for a specific product by its unique identifier (UID).

        Args:
            uid (str): The unique identifier of the product whose dependencies are to be fetched.

        Returns:
            dict: A dictionary containing the dependency information of the specified product.

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
        """
        url = f"{self.base_url}/get-product-dependency/{uid}"
        response = self._get(url, {})
        results = response.json()
        return results
    
    def set_status(self, product_ids: List, status_code: str):
        """
        Sets the status of a specified entity.

        Args:
            entity (str): The name of the entity whose status is to be set.
            uid (str): The unique identifier of the entity.
            status_code (str): The status code to set for the entity.

        Returns:
            dict: The JSON response from the server after setting the status.
        """
        payload = {
            "product_ids": product_ids,
            "status": status_code,
            "username": self.username,
        }
        url = f"{self.base_url}/set-status"
        response = self._patch(url, payload)
        return response.json()
