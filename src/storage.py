import pyrebase
import config.pyrebase_config as pyrebase_config


firebase = pyrebase.initialize_app(pyrebase_config.pirebaseConfig)
storage = firebase.storage()
file = "img.jpg"

def upload(filename, *path):
    a = storage.child("tutu.jpg")
    storage.child("tutu.jpg").put(file)

storage.child("tutu.jpg").download("dodo.jpg")