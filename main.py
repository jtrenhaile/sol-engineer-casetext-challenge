import requests
import os
import random
import getpass


def generate_auth_token(user, password):
    headers = {
        'Content-Type': 'application/json',
    }
    data = f'{{"email":"{user}","password":"{password}"}}'

    response = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/auth/login', headers=headers, data=data)

    return response.json()["token"]


def create_collection(collection_name, auth_token):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json',
    }

    data = '{ "model": "lawbert" }'

    response = requests.post(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}/create', headers=headers)
    return response.ok


def load_random_opinions(collection_name, file_directory, file_count, auth_token):
    headers = {
        'Authorization': "Bearer " + auth_token
    }

    opinions_filenames = os.listdir(file_directory)
    for filename in random.sample(opinions_filenames, file_count):
        print(filename)
        with open(os.path.join(file_directory, filename), "r") as curr_file:
            files = {
                'file': (filename+".txt", curr_file),
            }
            response = requests.post(f'https://project-apollo-api.stg.gc.casetext.com/v0/{collection_name}', headers=headers, files=files)
            if response.ok:
                print("Upload completed successfully!")
                print(response.text)
            else:
                print("Something went wrong while uploading a file!")


if __name__ == '__main__':
    collection_name = "[COLLECTION_NAME]"
    opinions_directory = "[FILES_DIRECTORY]"
    count = 1000
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    auth_token = generate_auth_token(username, password)
    collection_created = create_collection(collection_name, auth_token)
    if collection_created:
        load_random_opinions(collection_name, opinions_directory, count, auth_token)
    else:
        print("Something went wrong while creating the collection!")
