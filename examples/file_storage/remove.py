import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config


firebase = pyrebase.initialize_app(config.pirebaseConfig)
storage = firebase.storage()


file = "test.txt"
online_file = "img.jpg"
remove(storage, file,"file","image","personneA")