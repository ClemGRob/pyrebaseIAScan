import sys
import os

current_path_wrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, current_path_wrapper)

import pyrebase_realtimedb
import pyrebase_auth
import pyrebase_file_storage
import pyrebase_message


def set_data(firebase_database,data, *path):
    """
    place data inside the realDB

    Args:
        firebase_database (firebase.Database): database
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return pyrebase_realtimedb.set_data(firebase_database,data, *path)

def remove_data(firebase_database,*path):
    """
    remove data from the realDB

    Args:
        firebase_database (firebase.Database): database

    Returns:
        _type_: _description_
    """
    return pyrebase_realtimedb.remove_data(firebase_database,*path)

def get_data(firebase_database,*path):
    """
    received data from the realDB

    Args:
        firebase_database (firebase.Database): database

    Returns:
        _type_: _description_
    """
    return pyrebase_realtimedb.get_data(firebase_database,*path)



def login(firebase_database,email, passwd):
    """
    create a user, ennable to use authentication required function such as upload and download.

    Args:
        firebase_database (firebase.Auth): database
        email (str): emain
        passwd (str): password

    Returns:
        _type_: _description_
    """
    return pyrebase_auth.login(firebase_database,email, passwd)




def upload(storage, filename, online_filename, user= None,*path):
    """
    upload a file on firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to upload, position is file root, or the file path must be in the variable
        online_filename (str): name of the file you want in the storage
        user (dict) : contains the informations of the user
        *path(list[str]): path of the file in the storage
    """
    return pyrebase_file_storage.upload(storage, filename, online_filename, user,*path)

def download(storage, filename, online_filename, user= None, *path):
    """download a file from the firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to download, position is file root, or the file path must be in the variable
        online_filename (str): name of the file in the storage
        user (dict) : contains the informations of the user
        *path(list[str]): path of the file in the storage
    """
    return pyrebase_file_storage.download(storage, filename, online_filename,user, *path)


def remove(storage, online_filename, *path):
    """
    remove a file from firebase storage
    not working

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        online_filename (str): name of the file in the storage
        *path(list[str]): path of the file in the storage
    """
    return pyrebase_file_storage.remove(storage, online_filename, *path)



def send_message(API_KEY, DEVICE_TOKEN,message_title,message_body,data_message):
    """
    send a message to a device

    Args:
        API_KEY (str): API_key of the server
        DEVICE_TOKEN (str): device's token who will get the message
        message_title (str): message's tittle
        message_body (str): message's body
        data_message (dict): message's content    
    Returns:
        _type_: _description_
    """

    return pyrebase_message.send_message(API_KEY, DEVICE_TOKEN,message_title,message_body,data_message)