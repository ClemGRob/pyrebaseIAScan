import pyrebase
import config as pyrebase_config



def set_data(firebase_database,data, *path):
    current_position = firebase_database
    for positions in path:
        current_position = current_position.child(positions)
    current_position.set(data)


def remove_data(firebase_database,*path):
    current_position = firebase_database
    for positions in path:
        current_position = current_position.child(positions)
    current_position.remove()


def get_data(firebase_database,*path):
    current_position = firebase_database
    for positions in path:
        current_position = current_position.child(positions)
    pyrebase_data = current_position.get()
    data = {}
    for only_data in pyrebase_data.each():
        data[only_data.key()]=only_data.val()
    return data
