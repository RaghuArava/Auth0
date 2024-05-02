##!/usr/bin/python3
##!/opt/freeware/bin/python3   

#Note : Need to change above shebang line if wouldn't like to run like <python3 scriptname.py>

import sys
import os
import requests
import argparse
import json


def get_token():
  """
  Obtains an access token for the Management API.
  """
  token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
  data = {
      'grant_type': 'client_credentials',
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'audience': f"https://{AUTH0_DOMAIN}/api/v2/"
  }
  response = requests.post(token_url, data=data)

  if response.status_code == 200:
    return response.json()["access_token"]
  else:
    print(f"Error getting token: {response.text}")
    return None

def create_user(data):
    """
    Creates a new user in Auth0.

    Args:
        data Dictionary with below key values pair ex:'{"email": "sam@gmail.com", "password": "Passw0rd12345", "connection": "Username-Password-Authentication"}'
        email (str): User's email address.
        password (str): User's password.
        connection (str, optional): Auth0 connection for the user. Defaults to "Username-Password-Auth".

    Returns:
        dict: User dictionary or None if error occurs.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    #data = {"email": email, "password": password, "connection": connection}
    url = BASE_URL + "users"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error creating user: {response.text}")
        return None


def update_user(data):
    """
    Updates a user's information in Auth0.

    Args:
        data Dictionary with below key values pair ex:'{"email": "sam1@gmail.com","user_id":"auth0|663217cb9aa50fa870b6b50d","name":"sam1"}'
        user_id (str): ID of the user to update.
        data (dict): Dictionary containing the update information (e.g., email, password).

    Returns:
        dict: Updated user dictionary or None if error occurs.
    """
    user_id = data["user_id"]
    
    #deleting the user_id section from json data since it is unusable
    del data["user_id"]  
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    url = BASE_URL + f"users/{user_id}"
    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error updating user: {response.text}")
        return None

def get_users(data):
    """
    Retrieves users from Auth0.

    Args:
        data (dict) with below values ,ex : '{"email": "sam1@gmail.com"}' or '{}'
        email (str, optional): Email to filter users by. Defaults to None.

    Returns:
        list: List of user dictionaries or None if error occurs.
    """
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = BASE_URL + "users"
    email = None

    if "email" in data:
        email = data["email"]
        url += f"?q=email:{email}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting users: {response.text}")
        return None


def delete_user(data):
    """
    Deletes a user from Auth0.

    Args:
        data (dict) with below key:values ,ex: '{"user_id":"auth0|663217cb9aa50fa870b6b50d"}
        user_id (str): ID of the user to delete.

    Returns:
        bool: True if successful, False otherwise.
    """
    user_id = data["user_id"]
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = BASE_URL + f"users/{user_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return True
    else:
        print(f"Error deleting user: {response.text}")
        return False

def main(argv):
    #Creating Parser object using argparse module
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--cred_file',required=True, help='Credential file path (E.g : -F /path/to/cred/file.json)',)
    parser.add_argument('-O', '--operation_type',required=True, help='Enter the operation type (E.g : -O create_user)',)
    parser.add_argument('-D', '--dataForOperation',required=True,help='Data in the form of Dict {key:value},(e.g.: -D {email:email,password:password,connection:Username-Password-Authentication})',)
    args = parser.parse_args()
  
    #accessing command line arguments
    operation_type = args.operation_type
    data_to_perform_operation = args.dataForOperation
    cred_file_path = args.cred_file

    #evaluating the dict from string
    data_to_perform_operation = eval(data_to_perform_operation)    

    # defining the global variables ,since we are going to use these variable in each operations
    global API_TOKEN
    global AUTH0_DOMAIN
    global CLIENT_ID
    global CLIENT_SECRET
    global BASE_URL

    cred_data = json.load(open(cred_file_path))
    
    #reading Credentials from command line json file 
    AUTH0_DOMAIN = cred_data["AUTH0_DOMAIN"]
    CLIENT_ID = cred_data["CLIENT_ID"]
    CLIENT_SECRET = cred_data["CLIENT_SECRET"]

    BASE_URL = f"https://{AUTH0_DOMAIN}/api/v2/"


    #getting API token from the method get_token 
    API_TOKEN = get_token()
    

    ####Note Function call starts Here####
    if operation_type in ["create_user","update_user","get_users","delete_user"]:
       operation_type = eval(operation_type)
       response = operation_type(data_to_perform_operation)
       print(response)
    else:
       print("Unknown operation since exiting")
       sys.exit(1)
    ####Note Function call ends Here####



    ##below commented section for better understanding only ,however we are commenting below section###
    """
    if operation_type ==  "create_user":
       response = create_user(data_to_perform_operation)
       print(response)

    elif operation_type ==  "update_user":
       response = update_user(data_to_perform_operation)
       print(response)

    elif operation_type ==  "get_users":
       response = get_users(data_to_perform_operation)
       print(response)

    elif operation_type ==  "delete_user":
       response = delete_user(data_to_perform_operation)
       print(response)
    """
    ##comment section end here###
  
   
if __name__ == "__main__":
    main(sys.argv[1:])
