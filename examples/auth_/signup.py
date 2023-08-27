import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config


firebase = pyrebase.initialize_app(config.pirebaseConfig)
auth=firebase.auth()
# user=signup(auth, "password2@password.password2","password")
user=signup(auth, "clementguellec@gmail.com","password")