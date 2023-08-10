import pyrebase
import pyrebase_config


firebase = pyrebase.initialize_app(pyrebase_config.pirebaseConfig)
storage = firebase.storage()
file = "img.jpg"

# storage.child("tutu.jpg").put(file)

storage.child("tutu.jpg").download("dodo.jpg")