import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config


firebase = pyrebase.initialize_app(config.pirebaseConfig)
storage = firebase.storage()
file = "img.jpg"
online_file = "img.jpg"

auth=firebase.auth()
user=login(auth, "test@tttttt.com","password")

print(download(storage, file, online_file,user))