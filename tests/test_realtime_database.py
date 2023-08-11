import sys
import os
import pyrebase
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.wrapper import *



pirebaseConfig = {
    "apiKey": "AIzaSyDO3WxB9x89iWt0kIOtbTYAPFA8k_VcVuU",
    "authDomain": "projetpyrebase.firebaseapp.com",
    "databaseURL" : "https://projetpyrebase-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "projetpyrebase",
    "storageBucket": "projetpyrebase.appspot.com",
    "messagingSenderId": "594850185050",
    "appId": "1:594850185050:web:d9ff6bd287eb39f7137d63",
    "measurementId": "G-SF30YGJJEN"
}




def test_init():
    firebase = pyrebase.initialize_app(pirebaseConfig)
    return firebase.database()




def test(db):
    data = {"test": "success"}
    position = ["my","position","to","value"]
    assert set_data(db,data, *position)== {"test":"success"}
    assert get_data(db,*position) == {"test":"success"}
    assert remove_data(db,*position) == None

test(test_init())