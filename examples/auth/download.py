import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config


firebase = pyrebase.initialize_app(config.pirebaseConfig)
storage = firebase.storage()
file = "file.txt"
# the file must be at the root of the project
online_file = "file.txt"

auth=firebase.auth()
user=login(auth, "password@password.password","password")

print(download(storage, file, online_file,user))