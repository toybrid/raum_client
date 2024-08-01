import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


def get_user_home():
    """
    This function returns the user's home directory path.

    Returns:str
    """
    return Path.home()

def get_token_file() -> Path:
    """
    This function returns the path to the token file.
    The token file is located in the user's home directory under the '.raum' directory.
    If the '.raum' directory does not exist, it will be created.

    Returns:
    Path: The path to the token file.
    """
    token_file = get_user_home().joinpath('.raum/token.json')
    token_file.parent.mkdir(parents=True, exist_ok=True)
    return token_file

def get_access_token() -> Optional[str]:
    """
    This function retrieves the access token for the Raum API.
    It first checks if the access token and refresh token are provided as environment variables.
    If not, it attempts to load the tokens from a JSON file located in the user's home directory.

    Returns:
    RaumToken: An instance of the RaumToken class containing the access and refresh tokens.
    None: If no access token is found.

    Raises:
    FileNotFoundError: If the token file does not exist.
    json.JSONDecodeError: If the token file contains invalid JSON data.
    """
    access_token = os.getenv('RAUM_AUTH_ACCESS_TOKEN', None)
    if access_token:
        return access_token
    
    tokens = None
    token_file = get_token_file()
    if token_file.exists():
        with open(token_file, 'r') as f:
            tokens = json.load(f)

        if tokens:
            return tokens.get('id')
        
    return None

def save_token(tokens) -> None:
    """
    This function saves the provided access and refresh tokens to a JSON file.
    The JSON file is located in the user's home directory under the '.raum' directory.
    If the '.raum' directory does not exist, it will be created.

    Parameters:
    tokens (dict): A dictionary containing the access and refresh tokens.
        The dictionary should have the following structure:
        {
            'access': str,
            'refresh': str
        }

    Returns:
    None
    """
    token_file = get_token_file()
    with open(token_file, 'w') as f:
        json.dump(tokens, f)

def curl_from_response(response) -> str:
    """
    This function generates a curl command from a given HTTP response.

    Parameters:
    response (requests.Response): The HTTP response object from which to generate the curl command.

    Returns: str
    """
    req = response.request
    method = req.method
    uri = req.url
    data = req.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    command = f"curl -X {method} -H {headers} -d '{data}' '{uri}'"
    return command

def dict_to_params(filters):
    par = ''
    for key, value in filters.items():
        if par!= '':
            par += '&'
        par += f'{key}={value}'
    return par