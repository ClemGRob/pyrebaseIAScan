"""
all function to manipulate the file storage
can store picture and text file
"""

def upload(storage, filename:str, online_filename:str,user = None, *path):
    """
    upload a file on firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to upload, position is file root, or the file path must be in the variable
        online_filename (str): name of the file you want in the storage
        *path(list[str]): path of the file in the storage
    """
    try:
        current_position = storage
        for position in path:
            current_position = current_position.child(position)
        if user == None:
            return current_position.child(online_filename).put(filename)
        return current_position.child(online_filename).put(filename, user['idToken'])
    except FileNotFoundError as e:
        print("file not found"+ str(e))
        return "file not found"+ str(e)
    except Exception as e:
            print("unknown issue, verify your internet connexion"+ str(e))
            return "unknown issue, verify your internet connexion"+ str(e)


def download(storage, filename:str, online_filename:str,user = None, *path):
    """download a file from the firebase storage

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        filename (str): name of the file you want to download, position is file root, or the file path must be in the variable
        online_filename (str): name of the file in the storage
        *path(list[str]): path of the file in the storage
    """
    try:
        current_position = storage
        for position in path:
            current_position = current_position.child(position)
        if user == None:
            return current_position.child(online_filename).download(filename)
        print("aaaa")
        return current_position.child(online_filename).download(filename, user['idToken'])
    except FileNotFoundError as e:
        print("file not found"+ str(e))
        return "file not found"+ str(e)
    except Exception as e:
            print("unknown issue, verify your internet connexion"+ str(e))
            return "unknown issue, verify your internet connexion"+ str(e)


def remove(storage, online_filename:str, *path):
    """
    remove a file from firebase storage
    not working

    Args:
        storage (pyrebase.storage): pyrebase storage object type, enable to interact with the pyrebase storage
        online_filename (str): name of the file in the storage
        *path(list[str]): path of the file in the storage
    """
    try:
        current_position = storage
        for position in path:
            current_position = current_position.child(position)
        current_position.delete(online_filename)
    except Exception as e:
        print("unknown issue, verify your internet connexion"+ str(e))
        return "unknown issue, verify your internet connexion"+ str(e)

