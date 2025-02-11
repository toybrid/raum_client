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
import requests
import os
import getpass
from pprint import pprint
from raum_client import utils
from raum_client.contants import DEFAULT_LIMIT, DEFAULT_OFFSET, DEFAULT_SORT

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
        auth_token = utils.get_access_token()
        if auth_token:
            os.environ['RAUM_AUTH_ACCESS_TOKEN'] = auth_token
            self.headers['Authorization'] = f"Bearer {auth_token}"

    # -------------------------------- Generic --------------------------------

    def _get(self, url, filters=None):
        """
        Sends a GET request to the specified URL with optional filters.

        Parameters:
        url (str): The URL to send the GET request to.
        filters (dict, optional): A dictionary of filters to apply to the request. Defaults to None.

        Returns:
        requests.Response: The response from the server.
        """
        if filters is None:
            filters = {
                "limit": 10,
                "offset": 0
            }
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
        if resp.status_code == 201:
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
        # print(f"Response: {resp.text}")
        if resp.status_code == 200:
            return resp
        else:
            raise ValueError(resp.text)

    def _delete(self):
        pass

    # -------------------------------- Authentication --------------------------------

    def _register_user(self, payload):
        """
        Registers a new user with the provided payload.

        Parameters:
        payload (dict): A dictionary containing the user's email, username, password, 
        first name, and last name.

        Returns:
        dict: The response data from the server. If the user registration is successful, 
        it returns a dictionary containing the created user's details. Otherwise, it 
        returns a dictionary containing the error message.
        """
        url = f"{self.base_url}/register-user"
        response = self.session.post(url, json=payload)
        return response.json()

    def create_account(self):
        """
        Creates a new user account by prompting the user for input.

        Returns:
        dict: The response data from the server. If the user creation is successful, 
        it returns a dictionary containing the created user's details. Otherwise, it 
        returns a dictionary containing the error message.
        """
        payload = {
        "email":input('Email: '),
        "username":input('Username: '),
        "password":getpass.getpass('Password: '),
        "first_name":input('First Name: '),
        "last_name":input('Last Name: ')
        }
        return self._register_user(payload)

    def login(self):
        """
        Authenticates the user by prompting the user for input.

        Returns:
        None
        """
        email = input('Email: ')
        password = getpass.getpass('Password: ')
        token = self.authenticate(email, password)
        self.headers['Authorization'] = f"Bearer {token.get('id')}"
        utils.save_token(token)

    def authenticate(self, email, password):
        """
        Authenticates the user with the provided email and password.

        Parameters:
        email (str): The user's email.
        password (str): The user's password.

        Returns:
        dict: The response data from the server. If the authentication is successful, 
        it returns a dictionary containing the user's token. Otherwise, it returns a 
        dictionary containing the error message.
        """
        url = f"{self.base_url}/login"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload)
        return response.json()
    
    def is_authorised(self):
        """
        Checks if the user is authorised to access the API.

        Returns:
        bool: True if the user is authorised, False otherwise.
        """
        url = f"{self.base_url}/is-authorised"
        response = self._get(url)
        return response.json()

    
    def get_users(self, filters=None, sort=['username'], limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of users based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the user 
        retrieval. Defaults to None, which retrieves all users.
        sort (list, optional): A list of strings representing the fields to sort the users by. 
        Defaults to sorting by 'username'.
        limit (int, optional): The maximum number of users to retrieve. Defaults to the 
        value of DEFAULT_LIMIT.
        offset (int, optional): The number of users to skip before starting to retrieve. 
        Defaults to 0.

        Returns:
        list: A list of dictionaries, each representing a user. If no users are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/get-users"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    # -------------------------------- Core --------------------------------

    
    def get_container_types(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of container types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the container type retrieval. 
            Defaults to None, which retrieves all container types.
        sort (list, optional): A list of fields to sort the container types by. Defaults to DEFAULT_SORT.
        limit (int, optional): The maximum number of container types to retrieve. Defaults to DEFAULT_LIMIT.
        offset (int, optional): The number of container types to skip before starting to retrieve. Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a container type. If no container types are found, 
            it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/container-type"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def get_relation_types(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of relation types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the relation type 
        retrieval. Defaults to None, which retrieves all relation types.

        Returns:
        list: A list of dictionaries, each representing a relation type. If no relation types are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/relation-type"
        response = self._post(url, data, params=params)
        return response.json()['items']

    
    def get_elements(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of elements based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the element 
        retrieval. Defaults to None, which retrieves all elements.
        sort (list, optional): A list of fields to sort the elements by. Defaults to DEFAULT_SORT.
        limit (int, optional): The maximum number of elements to retrieve. Defaults to DEFAULT_LIMIT.
        offset (int, optional): The number of elements to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing an element. If no elements are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/element"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def get_data_types(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of data types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the data type 
        retrieval. Defaults to None, which retrieves all data types.
        sort (list, optional): A list of fields to sort the data types by. Defaults to DEFAULT_SORT.
        limit (int, optional): The maximum number of data types to retrieve. Defaults to DEFAULT_LIMIT.
        offset (int, optional): The number of data types to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a data type. If no data types are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/data-type"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def get_steps(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of steps based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the step retrieval. 
        Defaults to None, which retrieves all steps.
        sort (list, optional): A list of fields to sort the steps by. Defaults to DEFAULT_SORT.
        limit (int, optional): The maximum number of steps to retrieve. Defaults to DEFAULT_LIMIT.
        offset (int, optional): The number of steps to skip before starting to retrieve. Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a step. If no steps are found, it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/step"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def get_statuses(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of statuses based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the status 
        retrieval. Defaults to None, which retrieves all statuses.

        sort (list, optional): A list of fields to sort the statuses by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of statuses to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of statuses to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a status. If no statuses are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/status"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def get_bundle_types(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of bundle types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the bundle type 
        retrieval. Defaults to None, which retrieves all bundle types.

        sort (list, optional): A list of fields to sort the bundle types by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of bundle types to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of bundle types to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a bundle type. If no bundle types are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }

        url = f"{self.base_url}/bundle-type"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    # -------------------------------- Project --------------------------------

    def create_project(self, code, label, client_name):
        """
        Creates a new project with the provided code, label, and client name.

        Parameters:
        code (str): The unique identifier for the project.
        label (str): The human-readable label for the project.
        client_name (str): The name of the client associated with the project.

        Returns:
        dict: The response data from the server. If the project creation is successful, 
        it returns a dictionary containing the created project's details. Otherwise, it 
        returns a dictionary containing the error message.
        """
        payload = {
            'code':code,
            'label':label,
            'client_name': client_name,
        }
        url = f"{self.base_url}/project"
        response = self._post(url, payload)
        return response.json()

    def update_project(self, payload):
        """
        Updates an existing project with the provided payload.

        Parameters:
        payload (dict): A dictionary containing the updated project details. It should 
        include the project's ID and any other fields that need to be updated.

        Returns:
        dict: The response data from the server. If the project update is successful, 
        it returns a dictionary containing the updated project's details. Otherwise, it 
        returns a dictionary containing the error message.
        """
        url = f"{self.base_url}/project/{payload['id']}"
        response = self._patch(url, payload=payload)
        # print(response)
        return response.json()

    def get_projects(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of projects based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the project 
        retrieval. Defaults to None, which retrieves all projects.

        sort (list, optional): A list of fields to sort the projects by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of projects to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of projects to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a project. If no projects are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/project-search"
        response = self._post(url, data, params=params)
        return response.json()['items']

    # -------------------------------- Container --------------------------------
    
    def create_container(self,
                         project,
                         container_type,
                         code,
                         client_name,
                         frame_range={}):
        """
        Creates a new container in the system.

        Parameters:
        project (dict): A dictionary representing the project to which the container belongs.
        container_type (dict): A dictionary representing the type of the container.
        code (str): A unique identifier for the container.
        client_name (str): The name of the client associated with the container.
        frame_range (dict, optional): A dictionary representing the frame range of the container. 
        Defaults to an empty dictionary.

        Returns:
        dict: A dictionary representing the newly created container.
        """
        url = f"{self.base_url}/container"
        payload = {
            'project_id': project['id'],
            'container_type_id': container_type['id'],
            'code': code,
            'client_name': client_name,
            'frame_range': frame_range
            }
        response = self._post(url, payload)
        return response.json()

    def update_container(self, payload):
        """
        Updates an existing container in the system.

        Parameters:
        payload (dict): A dictionary representing the updated container details. It should 
        include the container's ID and any other fields that need to be updated.

        Returns:
        dict: A dictionary representing the updated container.
        """
        url = f"{self.base_url}/container/{payload['id']}"
        response = self._patch(url, payload)
        return response.json()

    def get_containers(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of containers based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the container 
        retrieval. Defaults to None, which retrieves all containers.

        sort (list, optional): A list of fields to sort the containers by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of containers to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of containers to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a container. If no containers are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/container-search"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    # -------------------------------- Container Relation --------------------------------

    def create_container_relation(self,
                                  container,
                                  relation_type,
                                  container_list
                                  ):
        """
        Creates a new container relation in the system.

        Parameters:
        container (dict): A dictionary representing the container from which the relation originates.
        relation_type (dict): A dictionary representing the type of the relation.
        container_list (list): A list of dictionaries representing the containers to which the relation points.

        Returns:
        dict: A dictionary representing the newly created container relation.
        """
        payload = {
            'from_container_id': container['id'],
            'relation_type_id': relation_type['id'],
            'to_containers': [i['id'] for i  in container_list]
        }
        url = f"{self.base_url}/container-relation"
        response = self._post(url, payload)
        return response.json()

    def update_container_relation(self, payload):
        """
        Updates an existing container relation in the system.

        Parameters:
        payload (dict): A dictionary representing the updated container relation details. It should 
        include the relation's ID and any other fields that need to be updated.

        Returns:
        dict: A dictionary representing the updated container relation.
        """
        url = f"{self.base_url}/container-relation/{payload['id']}"
        payload_dict = {}
        payload_dict['id'] = payload['id']
        payload_dict['from_container_id'] = payload['from_container']['id']
        payload_dict['relation_type_id'] = payload['relation_type']['id']
        payload_dict['to_containers'] =[ x['id'] for x in payload['to_containers']]
        response = self._patch(url, payload_dict)
        return response.json()

    def get_container_relation(self, container, relation):
        """
        Retrieves a container relation based on the provided container and relation.

        Parameters:
        container (dict): A dictionary representing the container from which the relation originates.
        relation (dict): A dictionary representing the relation type.

        Returns:
        dict: A dictionary representing the container relation. If no relation is found, it returns None.
        """
        url = f"{self.base_url}/container-relation/{container['id']}/{relation['id']}"
        response = self._get(url)
        return response.json()

    # -------------------------------- Products --------------------------------

    def create_product(self, 
                       container,
                       step,
                       element,
                       data_type,
                       lod,
                       layer,
                       extension,
                       version=None,
                       frame_range={},
                       filepath=None,
                       task='',
                       metadata={}):
        """
        Creates a new product in the system.

        Parameters:
        container (dict): A dictionary representing the container to which the product belongs.
        step (dict): A dictionary representing the step of the product.
        element (dict): A dictionary representing the element of the product.
        data_type (dict): A dictionary representing the data type of the product.
        lod (int): The level of detail of the product.
        layer (str): The layer of the product.
        version (str, optional): The version of the product. Defaults to None.
        frame_range (dict, optional): A dictionary representing the frame range of the product. 
        Defaults to an empty dictionary.
        filepath (str, optional): The file path of the product. Defaults to None.
        task (str, optional): The task of the product. Defaults to an empty string.
        extension (str, optional): The extension of the product. Defaults to an empty string.
        metadata (dict, optional): A dictionary representing the metadata of the product. 
        Defaults to an empty dictionary.

        Returns:
        dict: A dictionary representing the newly created product.
        """
        url = f"{self.base_url}/product"
        payload = {
            'container_id': container['id'],
            'step_id': step['id'],
            'element_id': element['id'],
            'data_type_id': data_type['id'],
            'lod': lod,
            'layer': layer,
            'frame_range': frame_range,
            'task': task,
            'extension': extension,
            'metadata': metadata
            }
        if version is not None:
            payload['version'] = version
        if filepath is not None:
            payload['filepath'] = filepath
        response = self._post(url, payload)
        return response.json()
        
    def update_product(self, payload):
        """
        Updates an existing product in the system.

        Parameters:
        payload (dict): A dictionary representing the updated product details. It should 
        include the product's ID and any other fields that need to be updated.

        Returns:
        dict: A dictionary representing the updated product.
        """
        url = f"{self.base_url}/product/{payload['id']}"
        response = self._patch(url, payload)
        return response.json()

    def get_products(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of products based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the product 
        retrieval. Defaults to None, which retrieves all products.

        sort (list, optional): A list of fields to sort the products by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of products to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of products to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a product. If no products are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/product-search"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def set_status(self, product, status):
        """
        Updates the status of an existing product in the system.

        Parameters:
        product (dict): A dictionary representing the product to update.
        status (str): The new status of the product.

        Returns:
        dict: A dictionary representing the updated product.
        """
        url = f"{self.base_url}/product/{product['id']}/{status}"
        response = self._patch(url)
        return response.json()
    
    def set_product_status(self, product, status):
        """
        Updates the status of an existing product in the system.

        Parameters:
        product (dict): A dictionary representing the product to update.
        status (str): The new status of the product.

        Returns:
        dict: A dictionary representing the updated product.
        """
        url = f"{self.base_url}/product/{product['id']}/{status}"
        response = self._patch(url)
        return response.json()
    
    
    # -------------------------------- Product Dependency --------------------------------
    def create_product_dependency(self,
                                product,
                                path_list
                                ):
        """
        Creates a new product dependency in the system.

        Parameters:
        product (dict): A dictionary representing the product to which the dependency belongs.
        path_list (list): A list of strings representing the file paths of the dependent products.

        Returns:
        dict: A dictionary representing the newly created product dependency.
        """
        payload = {
            'product': product['id'],
            'dependencies': path_list
        }
        url = f"{self.base_url}/product-dependency"
        response = self._post(url, payload)
        return response.json()

    def get_product_dependency(self, product):
        """
        Retrieves the product dependencies for a given product.

        Parameters:
        product (dict): A dictionary representing the product for which the dependencies are retrieved.

        Returns:
        list: A list of dictionaries, each representing a product dependency.
        """
        url = f"{self.base_url}/product-dependency/{product['id']}"
        response = self._get(url)
        return response.json()
    
    # -------------------------------- Bundles --------------------------------

    def create_bundle(self, container, step, bundle_type, products, version=None, description=None):
        """
        Creates a new bundle in the system.

        Parameters:
        container (dict): A dictionary representing the container to which the bundle belongs.
        step (dict): A dictionary representing the step of the bundle.
        bundle_type (dict): A dictionary representing the type of the bundle.
        products (list): A list of dictionaries representing the products included in the bundle.
        version (str, optional): The version of the bundle. Defaults to None.

        Returns:
        dict: A dictionary representing the newly created bundle.
        """
        url = f"{self.base_url}/bundle"
        payload = {
            'container_id': container['id'],
            'bundle_type_id': bundle_type['id'],
            'step_id': step['id'],
            'products': [i['id'] for i in products]
            }
        if version is not None:
            payload['version'] = version

        if description is not None:
            payload['description'] = description


        response = self._post(url, payload)
        return response.json()

    def update_bundle(self, payload):
        """
        Updates an existing bundle in the system.

        Parameters:
        payload (dict): A dictionary containing the updated bundle details. It should 
        include the bundle's ID and any other fields that need to be updated.

        Returns:
        dict: A dictionary representing the updated bundle.
        """
        url = f"{self.base_url}/bundle/{payload['id']}"
        payload_dict = {}
        payload_dict['id'] = payload['id']
        payload_dict['container_id'] = payload['container']
        payload_dict['step_id'] = payload['step']['id']
        payload_dict['bundle_type_id'] = payload['bundle_type']['id']
        payload_dict['products'] = payload['products']
        payload_dict['description'] = payload['description']
        response = self._patch(url, payload_dict)
        return response.json()

    def get_bundles(self, filters=None, sort=DEFAULT_SORT, limit=DEFAULT_LIMIT, offset=DEFAULT_OFFSET):
        """
        Retrieves a list of bundles based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the bundle 
        retrieval. Defaults to None, which retrieves all bundles.

        sort (list, optional): A list of fields to sort the bundles by. Defaults to DEFAULT_SORT.

        limit (int, optional): The maximum number of bundles to retrieve. Defaults to DEFAULT_LIMIT.

        offset (int, optional): The number of bundles to skip before starting to retrieve. 
        Defaults to DEFAULT_OFFSET.

        Returns:
        list: A list of dictionaries, each representing a bundle. If no bundles are found, 
        it returns an empty list.
        """
        data = {
            "filters": filters,
            "sort": sort
        }
        params = {
            "limit": limit,
            "offset": offset
        }
        url = f"{self.base_url}/bundle-search"
        response = self._post(url, data, params=params)
        return response.json()['items']
    
    def set_bundle_status(self, bundle, status):
        url = f"{self.base_url}/bundle/{bundle['id']}/{status}"
        response = self._patch(url)
        return response.json()