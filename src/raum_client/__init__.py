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
from raum_client import utils
import getpass

class Client:
    def __init__(self):
        self.base_url = os.getenv(
                                'RAUM_SERVER_BASE_URL', 
                                'http://localhost:8000/api/v1'
                                )
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
        auth_token = utils.get_access_token()
        if auth_token:
            self.headers['Authorization'] = f"Bearer {auth_token}"

    # -------------------------------- Generic --------------------------------

    def _get(self, url, filters=None):
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


    def _post(self, url, payload):
        resp = self.session.post(url, json=payload, headers=self.headers)
        if resp.status_code == 201:
            return resp
        else:
            raise ValueError(resp.text)


    def _patch(self, url, payload=None):
        resp = self.session.patch(url, json=payload, headers=self.headers)
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
    
    def get_users(self, filters=None):
        """
        Retrieves a list of users based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the user retrieval. 
        Defaults to None, which retrieves all users.

        Returns:
        list: A list of dictionaries, each representing a user. If no users are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/get-users"
        response = self._get(url, filters)
        return response.json()['items']
    
    # -------------------------------- Core --------------------------------

    
    def get_container_types(self, filters=None):
        """
        Retrieves a list of container types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the container type 
        retrieval. Defaults to None, which retrieves all container types.

        Returns:
        list: A list of dictionaries, each representing a container type. If no container 
        types are found, it returns an empty list.
        """
        url = f"{self.base_url}/container-type"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_relation_types(self, filters=None):
        """
        Retrieves a list of relation types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the relation type 
        retrieval. Defaults to None, which retrieves all relation types.

        Returns:
        list: A list of dictionaries, each representing a relation type. If no relation 
        types are found, it returns an empty list.
        """
        url = f"{self.base_url}/relation-type"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_elements(self, filters=None):
        """
        Retrieves a list of elements based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the element retrieval. 
        Defaults to None, which retrieves all elements.

        Returns:
        list: A list of dictionaries, each representing an element. If no elements are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/element"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_data_types(self, filters=None):
        """
        Retrieves a list of data types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the data type retrieval. 
        Defaults to None, which retrieves all data types.

        Returns:
        list: A list of dictionaries, each representing a data type. If no data types are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/data-type"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_steps(self, filters=None):
        """
        Retrieves a list of steps based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the step retrieval. 
        Defaults to None, which retrieves all steps.

        Returns:
        list: A list of dictionaries, each representing a step. If no steps are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/step"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_statuses(self, filters=None):
        """
        Retrieves a list of statuses based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the status retrieval. 
        Defaults to None, which retrieves all statuses.

        Returns:
        list: A list of dictionaries, each representing a status. If no statuses are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/status"
        response = self._get(url, filters)
        return response.json()['items']
    
    def get_bundle_types(self, filters=None):
        """
        Retrieves a list of bundle types based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the bundle type 
        retrieval. Defaults to None, which retrieves all bundle types.

        Returns:
        list: A list of dictionaries, each representing a bundle type. If no bundle 
        types are found, it returns an empty list.
        """
        url = f"{self.base_url}/bundle-type"
        response = self._get(url, filters)
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
        return response

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
        return response

    def get_projects(self, filters=None):
        """
        Retrieves a list of projects based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary of filters to apply to the project 
        retrieval. Defaults to None, which retrieves all projects.

        Returns:
        list: A list of project dictionaries. Each dictionary contains the details of 
        a single project. If no projects are found, it returns an empty list.
        """
        url = f"{self.base_url}/project"
        response = self._get(url, filters)
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

    def get_containers(self, filters=None):
        """
        Retrieves a list of containers based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the container 
        retrieval. Defaults to None, which retrieves all containers.

        Returns:
        list: A list of dictionaries, each representing a container. If no containers are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/container"
        response = self._get(url, filters)
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
                       version=None,
                       frame_range={},
                       filepath=None,
                       task='',
                       extension='',
                       meatadata={}):
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
        meatadata (dict, optional): A dictionary representing the metadata of the product. 
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
            'meatadata': meatadata
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

    def get_products(self, filters=None):
        """
        Retrieves a list of products based on the provided filters.

        Parameters:
        filters (dict, optional): A dictionary representing the filters to apply to the product 
        retrieval. Defaults to None, which retrieves all products.

        Returns:
        list: A list of dictionaries, each representing a product. If no products are found, 
        it returns an empty list.
        """
        url = f"{self.base_url}/product"
        response = self._get(url, filters)
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
    
    # -------------------------------- Product Dependency --------------------------------

    def create_bundle(self, container, bundle_type, products, version=None):
        url = f"{self.base_url}/bundle"
        payload = {
            'container_id': container['id'],
            'bundle_type_id': bundle_type['id'],
            'products': [i['id'] for i in products]
            }
        if version is not None:
            payload['version'] = version

        response = self._post(url, payload)
        return response.json()

    def update_bundle(self, payload):
        url = f"{self.base_url}/bundle/{payload['id']}"
        payload_dict = {}
        payload_dict['id'] = payload['id']
        payload_dict['container_id'] = payload['container']
        payload_dict['bundle_type_id'] = payload['bundle_type']
        payload_dict['products'] = [i['id'] for i in payload['products']]
        response = self._patch(url, payload_dict)
        return response.json()

    def get_bundles(self, filters=None):
        url = f"{self.base_url}/bundle"
        response = self._get(url, filters)
        return response.json()['items']