import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pyrebase
from src.wrapper import *
import config


firebase = pyrebase.initialize_app(config.pirebaseConfig)
storage = firebase.storage()
file = "test.txt"
online_file = "test.txt"

auth=firebase.auth()
user=login(auth, "password@password.password","password")



upload(storage, file, online_file, user,"file","image","personneA")