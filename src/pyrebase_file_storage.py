import pyrebase
import config.pyrebase_config as pyrebase_config


def upload(storage, filename, online_filename, *path):
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.child(online_filename).put(filename)

def download(storage, filename, online_filename, *path):
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.child(online_filename).download(filename)

def remove(storage, online_filename, *path):
    current_position = storage
    for position in path:
        current_position = current_position.child(position)
    current_position.delete(online_filename)
