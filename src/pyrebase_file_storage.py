"""
all function to manipulate the file storage
can store picture and text file
"""

import pyrebase
import config.pyrebase_config as pyrebase_config


def upload(storage, filename:str, online_filename:str, *path):
    """
    upload a file on firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to upload, position is file root, or the file path must be in the variable
        online_filename (str): name of the file you want in the storage
        *path(list[str]): path of the file in the storage
    """
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.child(online_filename).put(filename)

def download(storage, filename:str, online_filename:str, *path):
    """download a file from the firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to download, position is file root, or the file path must be in the variable
        online_filename (str): name of the file in the storage
        *path(list[str]): path of the file in the storage
    """
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.child(online_filename).download(filename)

def remove(storage, online_filename:str, *path):
    """
    remove a file from firebase storage
    not working

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        online_filename (str): name of the file in the storage
        *path(list[str]): path of the file in the storage
    """
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.delete(online_filename)
