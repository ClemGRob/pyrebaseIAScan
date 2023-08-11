import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config

firebase = pyrebase.initialize_app(config.pirebaseConfig)
db = firebase.database()

data = {"test": "success"}
set_data(db,data,"my","position","to","value")