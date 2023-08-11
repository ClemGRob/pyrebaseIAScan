"""
all the function to work with the realtime database
the realtime database is organised like JSON
"""

def set_data(firebase_database,data:dict, *path):
    """
    insert data in the realtime database
    Args:
        firebase_database (pyrebase.database): pyrebase database object type, enable to interact with the realtime database
        data (dict): information you want to add
    """
    try:
        current_position = firebase_database
        for position in path:
            current_position = current_position.child(position)
        return current_position.set(data)
    except Exception as e:
            print("unknown issue, verify your internet connexion"+ str(e))
            return "unknown issue, verify your internet connexion"+ str(e)

def remove_data(firebase_database,*path):
    """
    remove a data in the realtime database
    Args:
        firebase_database (pyrebase.database): _description_
    """
    try:
        current_position = firebase_database
        for position in path:
            current_position = current_position.child(position)
        return current_position.remove()
    except Exception as e:
        print("unknown issue, verify your internet connexion"+ str(e))
        return "unknown issue, verify your internet connexion"+ str(e)

def get_data(firebase_database,*path):
    """_summary_

    Args:
        firebase_database (pyrebase.database): _description_

    Returns:
        _type_: _description_
    """
    try:
        current_position = firebase_database
        for position in path:
            current_position = current_position.child(position)
        pyrebase_data = current_position.get()
        data = {}
        for only_data in pyrebase_data.each():
            data[only_data.key()]=only_data.val()
        return data
    except TypeError as e:
        print("no data to remove : "+str(e))
        return "no data to remove : "+str(e)
    except ConnectionError as e:
        print("Erreur de connexion:"+str(e))
        return "Erreur de connexion:"+str(e)
    except Exception as e:
        print("unknown issue, verify your internet connexion"+ str(e))
        return "unknown issue, verify your internet connexion"+ str(e)