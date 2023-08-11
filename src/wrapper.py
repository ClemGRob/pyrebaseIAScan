import sys
import os

current_path_wrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, current_path_wrapper)

import pyrebase_realtimedb
import pyrebase_auth



def set_data(firebase_database,data, *path):
    return pyrebase_realtimedb.set_data(firebase_database,data, *path)

def remove_data(firebase_database,*path):
    return pyrebase_realtimedb.remove_data(firebase_database,*path)

def get_data(firebase_database,*path):
    return pyrebase_realtimedb.get_data(firebase_database,*path)



def signup(firebase_database,email, passwd):
    return pyrebase_auth.signup(firebase_database,email, passwd)

def login(firebase_database,email, passwd):
    return pyrebase_auth.login(firebase_database,email, passwd)